path=$HOME"/Dropbox/Projects/Programming/Git/temporary-promotions-md"

############
# For Life #
############
if [ "$(whoami)" == "martinbernstorff" ]; then
        /Library/Frameworks/Python.framework/Versions/3.7/bin/python3 $path/promote.py -r "/System/Volumes/Data/Users/martinbernstorff/Dropbox/Life Lessons/"
fi


############
# For Work #
############
if [ "$(whoami)" == "martin-work" ]; then
        /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 $path/promote.py -r "/System/Volumes/Data/Users/martin-work/Dropbox/Work Lessons/"
fi
