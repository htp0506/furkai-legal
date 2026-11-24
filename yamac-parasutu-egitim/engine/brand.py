"""Marka ayarları. Kulüp adını/logosunu buradan ya da ortam değişkenleriyle değiştirin."""
import os
import skia

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Brand:
    line1 = os.environ.get("BRAND_LINE1", "DERİN YAMAÇ")
    line2 = os.environ.get("BRAND_LINE2", "SPOR KULÜBÜ · MERZİFON")
    full = os.environ.get("BRAND_FULL", "Derin Yamaç Spor Kulübü")
    handle = os.environ.get("BRAND_HANDLE", "@derinyamacsporkulubu")
    city = os.environ.get("BRAND_CITY", "Merzifon · Amasya")
    logo_path = os.environ.get("BRAND_LOGO", os.path.join(ROOT, "assets", "brand", "logo.jpg"))
    _img = None
    _tried = False

    def logo_image(self):
        if not self._tried:
            self._tried = True
            if self.logo_path and os.path.exists(self.logo_path):
                self._img = skia.Image.open(self.logo_path)
        return self._img


BRAND = Brand()
