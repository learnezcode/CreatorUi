from g4f.client import Client
import time

class RequestException(Exception):
    pass

class LiteGPT:
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the LiteGPT client using the g4f library.
        :param model: The model to use (default: gpt-4o-mini).
        """
        self.model = model
        self.client = Client()

    def answer(self, params):
        """
        Send a request to the model via g4f and return the response.
        :param params: A dictionary containing the transformed messages.
        :return: The model's response in the expected format.
        """
        while True:
            try:
                # Prepare the data for g4f
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=params,
                    web_search=False  # Disable web search as per requirements <button class="citation-flag" data-index="8">
                )
                # Format the response to match the expected structure
                formatted_response = {
                    "choices": [
                        {
                            "message": {
                                "content": response.choices[0].message.content
                            }
                        }
                    ]
                }
                return formatted_response
            except Exception as e:
                print(f"Error occurred: {e}. Retrying in 60 seconds...")
                time.sleep(60)