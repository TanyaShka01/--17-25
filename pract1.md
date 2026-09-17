## Задание 1: 
''' grep -v '^#' /etc/protocols | awk 'NF>=2 {printf "%-4d%s\n", $2, $
1}' | sort -rn | head -5 '''
