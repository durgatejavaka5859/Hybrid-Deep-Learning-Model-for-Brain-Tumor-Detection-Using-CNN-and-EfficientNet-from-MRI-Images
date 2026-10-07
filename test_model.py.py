import keras

class SafeDense(keras.layers.Dense):
    def __init__(self, **kwargs):
        kwargs.pop("quantization_config", None)
        super().__init__(**kwargs)

print("Loading model...")

model = keras.models.load_model(
    "brain_tumor_model_fixed.h5",
    compile=False,
    custom_objects={"Dense": SafeDense}
)

print("MODEL LOADED SUCCESSFULLY!")
model.summary()