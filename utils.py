class PDF(object):
    def __init__(self, pdf, size=(1080,720)):
        self.pdf = pdf
        self.size = size

    def _repr_html_(self):
        return f'<iframe src={self.pdf} width={self.size[0]} height={self.size[1]}></iframe>'

    def _repr_latex_(self):
        return fr'\includegraphics[width=1.0\textwidth]{{{self.pdf}}}'