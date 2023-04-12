# Import the 're' and 'setuptools' modules
import re
from setuptools import setup, find_packages

# Check if Python version is 3.x
if sys.version_info.major != 3:
    print('This Python is only compatible with Python 3, but you are running '
          'Python {}. The installation will likely fail.'.format(sys.version_info.major))

# Define extra dependencies for testing and MPI support
extras = {
    'test': [
        'filelock',
        'pytest',
        'pytest-forked',
        'atari-py',
        'matplotlib',
        'pandas'
    ],
    'mpi': [
        'mpi4py'
    ]
}

# Combine all extra dependencies into a single list
all_deps = []
for group_name in extras:
    all_deps += extras[group_name]

# Add a new 'all' group with all dependencies
extras['all'] = all_deps

# Set up the package with required dependencies and extras
setup(name='baselines',
      packages=[package for package in find_packages()
                if package.startswith('baselines')],
      install_requires=[
          'gym>=0.15.4, <0.16.0',
          'scipy',
          'tqdm',
          'joblib',
          'cloudpickle',
          'click',
          'opencv-python'
      ],
      extras_require=extras,
      description='OpenAI baselines: high quality implementations of reinforcement learning algorithms',
      author='OpenAI',
      url='https://github.com/openai/baselines',
      author_email='gym@openai.com',
      version='0.1.6')

# Check that TensorFlow is installed with a version above 1.4
import pkg_resources
tf_pkg = None
for tf_pkg_name in ['tensorflow', 'tensorflow-gpu', 'tf-nightly', 'tf-nightly-gpu']:
    try:
        tf_pkg = pkg_resources.get_distribution(tf_pkg_name)
    except pkg_resources.DistributionNotFound:
        pass
assert tf_pkg is not None, 'TensorFlow needed, of version above 1.4'
from distutils.version import LooseVersion
assert LooseVersion(re.sub(r'-?rc\d+$', '', tf_pkg.version)) >= LooseVersion('1.4.0')
