

class TransformerRecognitionModel(RecognitionModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._MLP = get_transformer_decoder()


class TransformerFeatureExtractor(RecurrentFeatureExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.model = get_transformer_encoder()
        self.H = self.model.config.d_model
        self.bidirectional = False # TODO unsure
