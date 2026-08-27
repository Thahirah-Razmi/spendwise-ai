import json
import re

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.tools import (
    add_expense,
    list_expenses,
    get_total_expenses,
    get_expenses_by_category,
)


MODEL_NAME = "Qwen/Qwen3-0.6B"


class LocalAI:

    def __init__(self):

        print(f"Loading {MODEL_NAME}...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype="auto",
            device_map="auto"
        )

        self.model.eval()

        print("Model loaded.")

        self.tool_map = {
            "add_expense": add_expense,
            "list_expenses": list_expenses,
            "get_total_expenses": get_total_expenses,
            "get_expenses_by_category": get_expenses_by_category,
        }

    def generate(self, messages):

        inputs = self.tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors="pt",
        return_dict=True,
        )

        inputs = {
            key: value.to(self.model.device)
            for key, value in inputs.items()
        }

        input_length = inputs["input_ids"].shape[-1]

        with torch.no_grad():

            output = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False,
            )

        generated = output[0][input_length:]

        response = self.tokenizer.decode(
            generated,
            skip_special_tokens=True
        )

        return response.strip()

    def extract_json(self, response):

        # Remove markdown code fences if the model adds them.
        response = response.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        # Try parsing the complete response first.
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try finding a JSON object inside the response.
        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if match:

            try:
                return json.loads(
                    match.group(0)
                )
            except json.JSONDecodeError:
                pass

        return None

    def classify_request(self, user_message):

        messages = [
            {
                "role": "system",
                "content": """
You are the command parser for SpendWise AI.

Your job is to convert the user's request into EXACTLY ONE JSON object.

You have these tools:

1. add_expense
Arguments:
- amount: number
- category: string
- description: string

2. list_expenses
Arguments:
{}

3. get_total_expenses
Arguments:
{}

4. get_expenses_by_category
Arguments:
- category: string

If the user wants to add an expense, use add_expense.

If the user wants to see their expenses, use list_expenses.

If the user asks how much they have spent in total, use get_total_expenses.

If the user asks how much they spent in a particular category, use get_expenses_by_category.

Return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not use XML.
Do not write anything outside the JSON.

Examples:

User:
Add $50 for groceries

Output:
{"tool":"add_expense","arguments":{"amount":50,"category":"groceries","description":"Grocery purchase"}}

User:
Show my expenses

Output:
{"tool":"list_expenses","arguments":{}}

User:
How much have I spent?

Output:
{"tool":"get_total_expenses","arguments":{}}

User:
How much did I spend on food?

Output:
{"tool":"get_expenses_by_category","arguments":{"category":"food"}}
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        response = self.generate(messages)

        print("\nMODEL OUTPUT:")
        print(response)

        parsed = self.extract_json(response)

        print("\nPARSED TOOL CALL:")
        print(parsed)

        return parsed

    def chat(self, user_message):

        tool_call = self.classify_request(
            user_message
        )

        if not tool_call:

            return {
                "response": (
                    "I couldn't understand that request. "
                    "Please try asking about adding or "
                    "viewing expenses."
                ),
                "tool_call": None
            }

        tool_name = tool_call.get("tool")

        arguments = tool_call.get(
            "arguments",
            {}
        )

        if tool_name not in self.tool_map:

            return {
                "response": (
                    f"Unknown tool: {tool_name}"
                ),
                "tool_call": tool_call
            }

        tool_function = self.tool_map[
            tool_name
        ]

        try:

            result = tool_function(
                **arguments
            )

        except Exception as error:

            return {
                "response": (
                    f"Tool execution failed: {error}"
                ),
                "tool_call": tool_call
            }

        return {
            "response": result,
            "tool_call": {
                "name": tool_name,
                "arguments": arguments,
                "result": result
            }
        }


ai = LocalAI()