
from setuptools import setup

setup(
    name="evogtk",
    version='0.9',
    description='Python GTK 2.x application development framework',
    author="Oliver Gutierrez",
    author_email="ogutsua@gmail.com",
    packages =['evogtk','evogtk.factories','evogtk.gui','evogtk.gui.accessclasslib','evogtk.gui.widgetlib','evogtk.tools'],
    platforms=['any'],
)