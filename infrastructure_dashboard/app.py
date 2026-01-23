"""
Main entry point for the Infrastructure Dashboard application
"""

from . import create_app


def main():
    """Run the Flask development server."""
    print("=" * 60)
    print("Nederwiek I Infrastructure Dashboard")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server\n")

    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)


if __name__ == '__main__':
    main()
