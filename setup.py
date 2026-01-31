from setuptools import setup, find_packages

setup(
    name="synova-ai",
    version="2.0.0",
    description="Synova AI - Quantum Consciousness Nexus",
    author="taylorgng0420-oss",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    install_requires=[
        "fastapi>=0.68.0,<1.0.0",
        "uvicorn[standard]>=0.15.0,<1.0.0",
        "python-dotenv>=0.19.0,<1.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "sqlalchemy>=2.0.0,<3.0.0",
        "alembic>=1.7.0,<2.0.0",
        "psycopg2-binary>=2.9.0,<3.0.0",
        "numpy>=1.21.0,<2.0.0",
        "pandas>=1.3.0,<2.0.0",
        "python-jose[cryptography]>=3.3.0,<4.0.0",
        "passlib[bcrypt]>=1.7.4,<2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-cov>=4.0.0,<5.0.0",
            "black>=23.0.0,<24.0.0",
            "isort>=5.12.0,<6.0.0",
            "mypy>=1.0.0,<2.0.0",
            "flake8>=6.0.0,<7.0.0",
        ],
        "ml": [
            "torch>=2.0.0,<3.0.0",
            "transformers>=4.30.0,<5.0.0",
        ],
    },
    python_requires=">=3.9,<3.12",
)
