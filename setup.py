import setuptools

setuptools.setup(
    name='auto_snorkel',
    version='1.0',
    author="Yilin Lu",
    author_email="22121281@zju.edu.cn",
    description="An open source toolkit for automatically generating labeling functions by language model.",
    url="https://github.com/thunlp/opennre",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    install_requires = [
        'numpy==1.18.5',
        'sklearn==0.22.1',
        'openai'
    ]
)