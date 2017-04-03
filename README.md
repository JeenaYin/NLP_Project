# NLP_Project

# Install NLTK with Standford Parser

cd $HOME

# Update / Install NLTK
pip install -U nltk

# Download the Stanford NLP tools
wget http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-04-20.zip
wget http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
# Extract the zip file.
unzip stanford-ner-2015-04-20.zip 
unzip stanford-parser-full-2015-04-20.zip 
unzip stanford-postagger-full-2015-04-20.zip


export STANFORDTOOLSDIR=$HOME

export CLASSPATH=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/stanford-postagger.jar:$STANFORDTOOLSDIR/stanford-ner-2015-04-20/stanford-ner.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar

export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-postagger-full-2015-04-20/models:$STANFORDTOOLSDIR/stanford-ner-2015-04-20/classifiers


# Organization of Files:

AnsweringSystem: Code for Answering System
QuestionSystem: Code for Question System
