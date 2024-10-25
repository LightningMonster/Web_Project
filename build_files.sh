echo "Build start"
python3.9 manage.py collectstatic --noinput --clear
echo "Build END"