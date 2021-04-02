from fastapi import FastAPI, HTTPException

from crypto.Asymmetric import Asymmetric
from crypto.CryptoError import CryptoError
from crypto.Symmetric import Symmetric
from crypto.Validator import Validator


class MyAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.private_key, self.public_key = Asymmetric.generate_key()
        self.symmetric_key = Symmetric.generate_key()

        @self.get("/symmetric/key")
        def get_symmetric_key():
            """
            Generate a new symmetric key
            """
            return {"key": Symmetric.generate_key()}

        @self.post("/symmetric/key")
        def set_symmetric_key(key: str):
            """
            Set the hex-encoded symmetric key on the server
            """
            try:
                Validator.symmetric_key(key)
            except CryptoError as e:
                raise HTTPException(status_code=400, detail=str(e))
            else:
                self.symmetric_key = key

        @self.post("/symmetric/encode")
        def symmetric_encode(text: str):
            """
            Encrypt text
            """
            return {"text": Symmetric.encrypt(text=text, key=self.symmetric_key)}

        @self.post("/symmetric/decode")
        def symmetric_decode(text: str):
            """
            Decrypt text
            """
            return {"text": Symmetric.decrypt(text=text, key=self.symmetric_key)}

        @self.get("/asymmetric/key")
        def get_asymmetric_key():
            """
            Generate a new asymmetric key and set it on the server
            """
            private_key, public_key = Asymmetric.generate_key()
            self.private_key, self.public_key = private_key, public_key
            return {"private key": private_key, "public key": public_key}

        @self.get("/asymmetric/key/ssh")
        def get_asymmetric_key_ssh():
            """
            Generate a new asymmetric key in OpenSSH format
            """
            private_key, public_key = Asymmetric.generate_key_openssh()
            return {"private key": private_key, "public key": public_key}

        @self.post("/asymmetric/key")
        def set_asymmetric_key(private_key: str, public_key: str):
            """
            Set the hex-encoded asymmetric key on the server
            """
            try:
                Validator.asymmetric_key(private_key=private_key, public_key=public_key)
            except CryptoError as e:
                raise HTTPException(status_code=400, detail=str(e))
            else:
                self.private_key, self.public_key = private_key, public_key

        @self.post("/asymmetric/sign")
        def sign(text: str):
            """
            Sign the text
            """
            return {"signature": Asymmetric.sign(text=text, private_key=self.private_key)}

        @self.post("/asymmetric/verify")
        def verify(signature: str, text: str):
            """
            Verify the text
            """
            if Asymmetric.verify(signature=signature, text=text, public_key=self.public_key):
                return {"detail": "verified"}
            else:
                raise HTTPException(status_code=400, detail="The text is not verified")

        @self.post("/asymmetric/encode")
        def asymmetric_encode(text: str):
            """
            Encrypt text
            """
            return {"text": Asymmetric.encrypt(text=text, public_key=self.public_key)}

        @self.post("/asymmetric/decode")
        def asymmetric_decode(text: str):
            """
            Decrypt text
            """
            return {"text": Asymmetric.decrypt(text=text, private_key=self.private_key)}
