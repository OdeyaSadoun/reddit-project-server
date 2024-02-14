class SentimentAnalysisError(Exception):
    pass


class PreprocessingError(SentimentAnalysisError):
    pass


class ModelInitializationError(SentimentAnalysisError):
    pass


class ModelPredictionError(SentimentAnalysisError):
    pass
