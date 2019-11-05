import numpy

class Dados():
    def __init__(self):
        self._faria_acordo_novamente = numpy.nan
        self._nota = numpy.nan

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def texto(self):
        return self._texto

    @texto.setter
    def texto(self, texto):
        self._texto = texto

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, hora):
        self._hora = hora

    @property
    def empresa(self):
        return self._empresa

    @empresa.setter
    def empresa(self, empresa):
        self._empresa = empresa

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, nota):
        self._nota = nota

    @property
    def faria_acordo_novamente(self):
        return self._faria_acordo_novamente

    @faria_acordo_novamente.setter
    def faria_acordo_novamente(self, faria_acordo_novamente):
        self._faria_acordo_novamente = faria_acordo_novamente