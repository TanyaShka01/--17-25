## Задание 1: 

grep -v '^#' /etc/protocols | awk 'NF>=2 {printf "%-4d%s\n", $2, $
1}' | sort -rn | head -5

## Задание 2:

grep -v '^#' /etc/protocols | awk 'NF>=2 {printf "%-4d%s\n", $2, $
1}' | sort -rn | head -5

## Задание 3:

nano reg
-------------------------
#! /bin/bash

text="$*"

len=${#text}

Line=$(printf '%*s' "$((len + 2))" '' | tr ' ' '-')
echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"
------------------------------

chmod +x banner
./banner "Hello from RTU MIREA!"

## Задание 5:

nano reg
-----------------------------

#!/bin/bash

if [ -z "$1" ]; then
    echo "Ошибка: Укажите имя программы для регистрации."
    echo "Использование: $0 <имя_программы>"
    exit 1
fi

PROGRAM_NAME="$1"
SOURCE_PATH="./$PROGRAM_NAME"
TARGET_DIR="/usr/local/bin"
TARGET_PATH="$TARGET_DIR/$PROGRAM_NAME"

if [ ! -f "$SOURCE_PATH" ]; then
    echo "Ошибка: Файл '$SOURCE_PATH' не найден в текущей директории."
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "Требуются права суперпользователя. Перезапуск с sudo..."
    exec sudo "$0" "$@"
    exit $?
fi

chmod 755 "$SOURCE_PATH"

cp "$SOURCE_PATH" "$TARGET_PATH"

if [ $? -eq 0 ]; then
    echo "Успех: Команда '$PROGRAM_NAME' зарегистрирована в $TARGET_DIR"
else
    echo "Ошибка: Не удалось скопировать файл в $TARGET_DIR"
    exit 1
fi

----------------------------------------------------------------

chmod +x reg
./reg banner
which banner

## Задание 6: 

nano check_comment.sh
-----------------------------------------------------------

#!/bin/bash

find . -type f \( -name "*.c" -o -name "*.js" -o -name "*.py" \) | while read -r file; do
    # Читаем первую строку файла
    first_line=$(head -n 1 "$file")
    
    if [[ "$first_line" =~ ^[[:space:]]*// ]] || [[ "$first_line" =~ ^[[:space:]]*# ]]; then
        echo "[ЕСТЬ КОММЕНТАРИЙ] $file"
    else
        echo "[НЕТ КОММЕНТАРИЯ] $file"
    fi
done

------------------------------------------------------------------

chmod +x check_comment.sh
./check_comment.sh

## Задание 7: 

nano find_dups.sh

-----------------------------------------------------------------

#!/bin/bash

if [ -z "$1" ]; then
    echo "Использование: $0 <путь_к_директории>"
    exit 1
fi

TARGET_DIR="$1"

find "$TARGET_DIR" -type f -exec md5sum {} + | sort | awk '
{
    hash=$1;
    $1="";
    file=$0;
    if (hash == prev_hash) {
        if (!printed) {
            print "Дубликаты (хеш: " prev_hash "):";
            print "  " prev_file;
            printed=1;
        }
        print "  " file;
    } else {
        printed=0;
    }
    prev_hash=hash;
    prev_file=file;
}'

---------------------------------------------------------------------

chmod +x find_dups.sh
./find_dups.sh /path/to/folder

## Задание 8:

nano archive_ext.sh

-----------------------------------------------------------------------

#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Использование: $0 <расширение> <имя_архива.tar>"
    echo "Пример: $0 txt backup.tar"
    exit 1
fi

EXT="$1"
ARCHIVE_NAME="$2"

find . -maxdepth 1 -type f -name "*.$EXT" -print0 | tar -cvf "$ARCHIVE_NAME" --null -T -

if [ $? -eq 0 ]; then
    echo "Архив '$ARCHIVE_NAME' успешно создан."
else
    echo "Ошибка при создании архива."
fi

-----------------------------------------------------------------------

chmod +x archive_ext.sh
./archive_ext.sh txt my_archive.tar

## Задание 9:

nano replace_spaces.sh

----------------------------------------------------------------------

#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Использование: $0 <входной_файл> <выходной_файл>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: Файл '$INPUT_FILE' не найден."
    exit 1
fi

sed 's/    /\t/g' "$INPUT_FILE" > "$OUTPUT_FILE"

echo "Готово! Результат сохранен в '$OUTPUT_FILE'."

-------------------------------------------------------------------

chmod +x archive_ext.sh
./archive_ext.sh txt my_archive.tar

## Задание 9:

nano replace_spaces.sh

------------------------------------------------------------------

#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Использование: $0 <входной_файл> <выходной_файл>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: Файл '$INPUT_FILE' не найден."
    exit 1
fi

sed 's/    /\t/g' "$INPUT_FILE" > "$OUTPUT_FILE"

echo "Готово! Результат сохранен в '$OUTPUT_FILE'."

------------------------------------------------------------------

chmod +x replace_spaces.sh
./replace_spaces.sh input.txt output.txt

## Задание 10:

nano find_empty.sh

-----------------------------------------------------------------

#!/bin/bash

if [ -z "$1" ]; then
    echo "Использование: $0 <директория>"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Ошибка: Директория '$TARGET_DIR' не найдена."
    exit 1
fi

echo "Пустые файлы в '$TARGET_DIR':"

find "$TARGET_DIR" -type f -empty -printf "%f\n"

------------------------------------------------------------------

chmod +x find_empty.sh
./find_empty.sh /path/to/folder
