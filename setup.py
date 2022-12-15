from setuptools import setup, find_packages

setup(name='plottools',
      version='1.0.0',
      description='A set of command line scripts for plotting data with python',
      url='https://github.com/Sp-ino/plottools',
      author='Valerio Spinogatti',
      author_email='spinovale97@gmail.com',
      license='GNU',
      packages=find_packages(),
      entry_points={'console_scripts' : ['basic_plot=plottools.basic_plot:main',
                                    'compute_fom_adc=plottools.compute_fom_adc:main',
                                    'fourier=plottools.fourier:main',
                                    'histogr=plottools.histogr:main',
                                    'multi_axes_plot=plottools.multi_axes_plot:main',
                                    'rms_discr=plottools.rms_discr:main']},
      install_requires=['matplotlib', 'numpy'],
      zip_safe=False)
