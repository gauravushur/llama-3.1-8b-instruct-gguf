from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import os

class InferlessPythonModel:
    def initialize(self):
        nfs_volume = os.getenv("NFS_VOLUME")
        if os.path.exists(nfs_volume + "/phi-4-Q4_K_M.gguf") == False :
            cache_file = hf_hub_download(
                                repo_id="unsloth/phi-4-GGUF",
                                filename="phi-4-Q4_K_M.gguf",
                                local_dir=nfs_volume)
        self.llm = Llama(
            model_path=f"{nfs_volume}/phi-4-Q4_K_M.gguf",
            main_gpu=0,
            n_gpu_layers=-1)

    def infer(self, inputs):
        prompt = inputs["prompt"]
        system_prompt = inputs.get("system_prompt","You are a friendly bot.")
        temperature = inputs.get("temperature",0.7)
        top_p = inputs.get("top_p",0.1)
        repeat_penalty = inputs.get("repeat_penalty",1.0)
        max_tokens = inputs.get("max_tokens",256)
        
        output = self.llm.create_chat_completion(
                    messages = [
                      {"role": "system", "content": f"{system_prompt}"},
                      {"role": "user","content": f"{prompt}"}],
                    temperature=temperature, top_p=top_p, repeat_penalty=repeat_penalty,max_tokens=max_tokens
        )
        text_result = output['choices'][0]['message']['content']
        
        return {'generated_result': text_result}
        
    def finalize(self):
        self.llm = None
