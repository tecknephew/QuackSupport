import anthropic
from anthropic.types.beta import BetaMessage, BetaTextBlock, BetaToolUseBlock
import os
from dotenv import load_dotenv
import logging

class AnthropicClient:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        try:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize Anthropic client: {str(e)}")
        
    def get_next_action(self, run_history) -> BetaMessage:
        try:
            # Convert BetaMessage objects to dictionaries
            cleaned_history = []
            for message in run_history:
                if isinstance(message, BetaMessage):
                    cleaned_history.append({
                        "role": message.role,
                        "content": message.content
                    })
                elif isinstance(message, dict):
                    cleaned_history.append(message)
                else:
                    raise ValueError(f"Unexpected message type: {type(message)}")
            
            response = self.client.beta.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=[
                    {
                        "type": "computer_20241022",
                        "name": "computer",
                        "display_width_px": 800, #1280
                        "display_height_px": 600, #800
                        "display_number": 1,
                    },
                    {
                        "name": "finish_run",
                        "description": "Call this function when you have achieved the goal of the task.",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "success": {
                                    "type": "boolean",
                                    "description": "Whether the task was successful"
                                },
                                "error": {
                                    "type": "string",
                                    "description": "The error message if the task was not successful"
                                }
                            },
                            "required": ["success"]
                        }
                    }
                ],
                messages=cleaned_history,
                system = """
The user will ask you to help them perform a computer settings related task, and you should guide them one step at a time. 
Give them clear instructions on what to do next in a detailed, visual manner. Always remember that the user is taking actions 
and that you only instruct them on which actions to take.

Explicitly tell the user the actions they should take:
'Take step X and go to Y...'

If the outcome is not correct, provide new, alternative advice. 
Only when you confirm that a step was executed correctly should you move on to the next one. 

You should always call a tool! Always return a tool call. 
The ONLY allowed tools are "mouse_move". Additionally remember to call the `finish_run` tool when the user has achieved the goal of the task and to call "screenshot" for the first call. 
Only call the `finish_run` tool when you have verified via a screenshot that the user has achieved the goal of the task.

Do not explain once the task is finished; just call the tool. 

When the user asks you to enable dark mode, here is what you will do:
Move to the gear wheel labelled "System Settings" to open up system settings. Then navigate to "Appearance" and enable dark mode.
Never open System Settings through any other way than the gear wheel icon on the Desktop.
Whenever an action requires you to open Settings, the first thing you will do is navigate to the gear wheel.
""",

                betas=["computer-use-2024-10-22"],
            )

            # If Claude responds with just text (no tool use), create a finish_run action with the message
            has_tool_use = any(isinstance(content, BetaToolUseBlock) for content in response.content)
            if not has_tool_use:
                text_content = next((content.text for content in response.content if isinstance(content, BetaTextBlock)), "")
                # Create a synthetic tool use block for finish_run
                response.content.append(BetaToolUseBlock(
                    id="synthetic_finish",
                    type="tool_use",
                    name="finish_run",
                    input={
                        "success": False,
                        "error": f"Claude needs more information: {text_content}"
                    }
                ))
                logging.info(f"Added synthetic finish_run for text-only response: {text_content}")

            return response
            
        except anthropic.APIError as e:
            raise Exception(f"API Error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
