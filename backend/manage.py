#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- BEGIN .env loading ---
try:
    from dotenv import load_dotenv
except ImportError:
    print("WARNING: python-dotenv not found. .env file will not be loaded.")
    load_dotenv = None # Define it as None if import fails

def load_env_vars_for_manage_py():
    if load_dotenv: # Check if load_dotenv was successfully imported
        # Determine the base directory (where manage.py is located)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(base_dir, '.env')
        if os.path.exists(env_path):
            print(f"manage.py: Loading environment variables from: {env_path}")
            load_dotenv(dotenv_path=env_path, override=True)
        else:
            print(f"manage.py WARNING: .env file not found at {env_path}")
    else:
        print("manage.py: Skipping .env loading as dotenv library is not available or import failed.")

# --- END .env loading ---


def main():
    """Run administrative tasks."""
    load_env_vars_for_manage_py() # Load .env variables at the start of main()
    
    # This should point to your settings file.
    # Given your current structure, 'settings' (referring to settings.py in the same directory) is correct.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main() 