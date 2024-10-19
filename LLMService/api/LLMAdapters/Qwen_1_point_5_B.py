import markdown2
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from ..models import ChatHistory


class Qwen_1_point_5_B:
    __default_message_array__ = [{"role": "system", "content": "You are a personal assistant that excels in programming tasks but can answer any question."}]
    __message_array__ = __default_message_array__.copy()
    __model_name__ = "Qwen/Qwen2.5-1.5B-Instruct"
    __model__ = None
    __tokenizer__ = None
    __device__ = None
    __response_array__ = []

    def __init__(self):
        self.__device__ = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model__ = AutoModelForCausalLM.from_pretrained(
            self.__model_name__,
            torch_dtype=torch.float32
        ).to(self.__device__)
        self.__tokenizer__ = AutoTokenizer.from_pretrained(self.__model_name__)

    def send_message(self, message):
        self.__message_array__.append({"role": "user", "content": message})
        self.__response_array__.append(self.__query_llm())
        return self.__response_array__[-1]

    def clear_context(self):
        for i in range(1, len(self.__message_array__)):
            user_message = self.__message_array__[i]['content']
            bot_response = self.__response_array__[i - 1]
            ChatHistory.objects.create(user_message=user_message, bot_response=bot_response)

        self.__message_array__ = self.__default_message_array__.copy()
        self.__response_array__ = []

    def get_history(self):
        result = []
        for i in range(len(self.__message_array__)):
            if i == 0:
                continue
            if len(self.__message_array__) < i:
                continue
            result.append({'message': self.__message_array__[i], 'response': markdown2.markdown(self.__response_array__[i-1])})
        return result

    def __query_llm(self):
        try:
            text = self.__tokenizer__.apply_chat_template(
                self.__message_array__,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.__tokenizer__([text], return_tensors="pt").to(
                self.__device__)  # Move input tensors to the same device as the model

            generated_ids = self.__model__.generate(
                **model_inputs,
                max_new_tokens=512
            )

            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = self.__tokenizer__.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return response

        except Exception as e:
            print(f"Error during LLM query: {str(e)}")
            return f"An error occurred: {str(e)}"