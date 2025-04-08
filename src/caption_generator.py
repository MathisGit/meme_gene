import os
import json
from mistralai import Mistral
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class CaptionGenerator:
    def __init__(self):
        """Initialize the caption generator with Mistral API."""
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-large-latest"
        
    def _create_caption_prompt(self, prompt: str, meme_info: Dict) -> str:
        """Create the prompt for caption generation."""
        format_instructions = {
            "two_panels": """Generate EXACTLY two short and funny texts that contrast well.
Example format for two_panels:
{
    "texts": ["First panel text", "Second panel text"]
}""",
            "three_panels": """Generate EXACTLY three short texts that tell a story.
Example format for three_panels:
{
    "texts": ["First panel text", "Second panel text", "Third panel text"]
}""",
            "top_bottom": """Generate EXACTLY two short texts: an attention-grabbing one at the top and a punchline at the bottom.
Example format for top_bottom:
{
    "texts": ["Top text", "Bottom text"]
}""",
            "single_caption": """Generate EXACTLY one short and funny caption that will be placed at the bottom of the image.
The caption MUST:
- Start with "When"
- Be short and impactful (max 6-7 words)
- Be in English
- Be funny and in meme style
- Be a little bit tacky, creative and viral

Example format for single_caption:
{
    "texts": ["When you push to prod on Friday"]
}"""
        }
        
        return f"""You are an expert in creating English memes. Generate a short and funny caption for the following meme.

User prompt: "{prompt}"

Meme information:
- Description: {meme_info['description']}
- Format: {meme_info['format']}

{format_instructions[meme_info['format']]}

IMPORTANT:
- The caption MUST start with "When"
- The caption must be VERY short (max 6-7 words)
- The response MUST be in English
- Use the exact JSON format as in the example
- Generate only the caption, no explanations
- Be impactful and funny
"""
        
    def generate_captions(self, prompt: str, meme_info: Dict) -> List[str]:
        """
        Generate captions for a meme from a prompt.
        
        Args:
            prompt (str): The prompt describing the situation
            meme_info (Dict): Information about the selected meme
            
        Returns:
            List[str]: The generated captions
        """
        caption_prompt = self._create_caption_prompt(prompt, meme_info)
        
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": caption_prompt,
                },
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse JSON response
        result = json.loads(response.choices[0].message.content)
        return result["texts"]
    
if __name__ == "__main__":
    generator = CaptionGenerator()
    prompt = "when you push to prod on Friday"
    meme_info = {
        "description": "A developer pushing code to prod on Friday",
        "format": "two_panels"
    }
    texts = generator.generate_captions(prompt, meme_info)
    print(texts)

