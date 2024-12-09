# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('C:/Users/tiffa/OneDrive - INACAP/Documents/Taller diseño/ServiceMatch/2/2/serviceMatch - copia/serviceMatch'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'serviceMatch.settings'
import django
django.setup()

title = 'Documentación ServiceMatch'
project = 'ServiceMatch'
version = '1.0'
copyright = '2024, Tiffani Bastidas, Francisco Pinol, Raquel Guarda'
author = 'Tiffani Bastidas'
release = '09 de Diciembre, 2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'rst2pdf.pdfbuilder',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
