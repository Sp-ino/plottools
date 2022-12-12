from setuptools import setup

setup(name='plottools',
      version='0.0.0',
      description='A set of command line scripts for plotting data with python',
      url='https://github.com/Sp-ino/plottools',
      author='Valerio Spinogatti',
      author_email='spinovale97@gmail.com',
      license='GNU',
      packages=[],
      scripts=['bin/basic_plot',
               'bin/compute_fom_adc',
               'bin/fourier',
               'bin/histogr',
               'bin/multi_axes_plot',
               'bin/rms_discr'],
      zip_safe=False)
