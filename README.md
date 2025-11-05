# 🍽️ Kitchenware Marketplace

A Django-based platform for buying and selling second-hand kitchenware items. Connect buyers and sellers in a trusted marketplace with user authentication, item listings, messaging, and transaction management.

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### ✅ Completed (Phase 1)
- **Project Setup**: Complete Django project with PostgreSQL database
- **Base Templates**: Bootstrap 5 responsive design with navigation
- **Environment Configuration**: Secure settings management
- **Documentation**: Comprehensive setup and development guides

### 🚧 In Development (Phase 2)
- **User Authentication**: Registration, login, profiles, seller accounts
- **Marketplace CRUD**: Item listings with image upload
- **Search & Filtering**: Advanced item discovery
- **Messaging System**: Direct buyer-seller communication
- **Transaction Management**: Purchase tracking and reviews

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional - defaults to SQLite)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kitchenwareTradingSite.git
cd kitchenwareTradingSite

# Run the setup script
./setup.sh

# Create superuser
source venv/bin/activate
python3 manage.py createsuperuser

# Start the development server
python3 manage.py runserver
```

**Visit**: http://localhost:8000/ (Homepage) or http://localhost:8000/admin/ (Admin Panel)

## 📖 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete setup guide
- **[docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** - Project scope and roadmap
- **[docs/README_DOCS.md](docs/README_DOCS.md)** - Documentation index
- **[POSTGRES_SETUP.md](POSTGRES_SETUP.md)** - Database setup
- **[SUPERUSER_GUIDE.md](SUPERUSER_GUIDE.md)** - Admin guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Development Guidelines
- Follow Django best practices
- Write descriptive commit messages
- Test your changes before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community discussions
- **Documentation**: Check the `docs/` folder for detailed guides

---

**Built with ❤️ using Django**

*Kitchenware Marketplace - Connecting kitchen enthusiasts since 2025*