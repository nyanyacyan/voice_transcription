# /bin/bash
'''  インストールするもの

Python3.8.10
homebrew
pip
requirements.txt
'''

echo "現在、Homebrewをインストール中です..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
if [ $? -eq 0 ]; then
    echo "Homebrewのインストールが成功しました。"
else
    echo "Homebrewのインストールに失敗しました。"
    exit 1
fi

echo "現在、Pythonをインストール中です..."
brew install python@3.8.10
if [ $? -eq 0 ]; then
    echo "Pythonのインストールが成功しました。"
else
    echo "Pythonのインストールに失敗しました。"
    exit 1
fi

echo "現在、pipをインストール中です..."
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
if [ $? -eq 0 ]; then
    echo "pipのインストールが成功しました。"
else
    echo "pipのインストールに失敗しました。"
    exit 1
fi

echo "現在、Pythonのパッケージをインストール中です..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
pip3 install -r "$DIR/requirements.txt"

if [ $? -eq 0 ]; then
    echo "Pythonのパッケージのインストールが成功しました。"
else
    echo "Pythonのパッケージのインストールに失敗しました。"
    exit 1
fi

echo "すべて完了しました。"

read