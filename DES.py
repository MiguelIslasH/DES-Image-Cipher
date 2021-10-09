from PIL import BmpImagePlugin
from Crypto.Cipher import DES
import hashlib

class DESCipher:
  def _prepareImage(self, imageURL: str) -> bytes: 
    try:
      self.input_image = BmpImagePlugin.BmpImageFile(imageURL)
      image_data = self.input_image.tobytes()
      return image_data
    except Exception as e:
      raise Exception(e)

  def _getMode(self, mode: int) -> int:
    if mode == 1:
      return DES.MODE_ECB, "ECB"
    elif mode == 2:
      return DES.MODE_CBC, "CBC"
    elif mode == 3:
      return DES.MODE_CFB, "CFB"
    elif mode == 4:
      return DES.MODE_OFB, "OFB"
    else:
      raise Exception("No supported DES mode")

  def _prepareDES(self, key: str, mode: int, iv = "12345678"):
    if len(key) != 8:
      raise Exception("Key must be 8 bytes long, not "+ len(key))

    key = key.encode('ascii')
    if mode == 1:
      des = DES.new(key, self._getMode(mode)[0])
    else:
      iv = iv.encode("ascii")
      hash=hashlib.sha256(iv) 
      p = hash.digest()
      iv = p.ljust(8)[:8]
      des = DES.new(key, self._getMode(mode)[0], iv)
    return des

  def _generateImage(self, text: str, imageURL: str, action: str, mode: int):
    output_image = self.input_image.copy()
    output_image.frombytes(text)
    try:
      imageName = imageURL.split(".")[0]
      imageName = imageName+action+self._getMode(mode)[1]+".bmp"
      output_image.save(imageName)
      return "image generated successfully as " + imageName
    except Exception as e:
      raise Exception(e)

  def encrypt(self, key: str, mode: int, imageURL: str, iv = "12345678" ) -> None:
    imageBytes = self._prepareImage(imageURL)
    des = self._prepareDES(key, mode, iv)
    encryptedText = des.encrypt(imageBytes)
    print(self._generateImage(encryptedText, imageURL, "e", mode))
    
  def decrypt(self, key: str, mode: int, imageURL: str, iv = "12345678") -> None:
    imageBytes = self._prepareImage(imageURL)
    des = self._prepareDES(key, mode, iv)
    decryptedText = des.decrypt(imageBytes)
    print(self._generateImage(decryptedText, imageURL, "d", mode))

desCipher = DESCipher()
desCipher.encrypt("holahola", 2, "Imagen1.bmp", "13579135")
desCipher.decrypt("holahola", 2, "Imagen1eCBC.bmp", "13579135")