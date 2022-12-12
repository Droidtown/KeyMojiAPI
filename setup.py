import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="KeyMojiAPI",
    version="1.0.5",
    author="Droidtown Linguistic Tech. Co. Ltd.",
    author_email="info@droidtown.co",
    description="""KeyMoji sentimental analysis system differs from other "amature-tagged" and "pure-ML/DL" text sentimental analysis solutions in many ways. KeyMoji combines "syntactic structure information", "formal semantics" and "lexical semantic model" in one calculating process to estimate the sentimental bias and distributions of sentiments in texts.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Droidtown/KeyMojiAPI",
    project_urls={
        "Documentation": "https://api.droidtown.co/KeyMojiAPI/document/",
        "Source": "https://github.com/Droidtown/KeyMojiAPI",
    },
    license="MIT License",
    keywords=[
        "emotion",
        "emotion recognition",
        "emotions in formula",
        "sentiment"
        "sentiment analyzer",
        "sentiment analysis",
        "sentiment detection",
        "NLP", "NLU", "AI",
        "artificial intelligence",
        "computational linguistics",
        "language",
        "linguistics",
        "natural language",
        "natural language processing",
        "natural language understanding",
        "parsing",
        "syntax",
        "text analytics"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "requests >= 2.25.1",
        "python-rapidjson >= 0.9.4",
        "matplotlib >= 3.3.3",
        "numpy >= 1.19.5",
        "scipy >= 1.5.4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        #"Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Information Technology",
        "Natural Language :: Chinese (Traditional)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Filters",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6.1",
)
