"""
TNW Dashboard - Entry point script
Provides a simple command-line interface to run the TNW dashboard
"""

from tnw_dashboard import create_app

# Create Flask application instance for gunicorn
app = create_app()

if __name__ == '__main__':
    from tnw_dashboard.app import main
    main()
