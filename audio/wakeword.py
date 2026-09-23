import openwakeword
from openwakeword import Model
class WakeWord:
    def __init__(self) -> None:
        openwakeword.utils.download_models()
        self.model = Model(
            wakeword_models=['models/Hey_Eva_20260923_012532.onnx'],
            inference_framework="onnx",
        )
    
    # Detect Wake word
    def detect(self, audio):
        prediction = self.model.predict(audio)
        
        for wakeword, score in prediction.items():
            if score > 0.5:
                return True

        return False
        