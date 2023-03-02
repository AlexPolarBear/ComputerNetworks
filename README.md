## Homework 2. ***Rest Service***
## 1. Программирование. Rest Service. Часть I 
### Задание А
### Задание Б
### Задание В
## 1. Задачки
### Задание 1
$\{L/R}$ - это время, необходимое для передачи 1 пакета по одному соединению.

Будем считать, что передача пакетов последовательна, т.е. второй пакет передается только после первого и т.д. Значит существует $\{P}$ таких задержек для передачи всех пакетов по одному такому соединению - $\{P*L/R}$.

Также, существует ещё и $\{N-1}$ таких задержек для передачи по оставшимся каналам, следовательно $\{(N-1)*L/R}$.

Тогда общая задержка для передачи все $\{P}$ пакетов составит:

$$\{P*L/R+(N-1)*L/R=(P+(N-1))*L/R}$$

<ins>Ответ:</ins> $\{(P+(N-1))*L/R}$
### Задание 2
Так как каналы расположенны последовательно, то время передачи от хоста А к хосту Б - сумма времени передачи на каждом участке.

$$\{t=L/R_1+L/R_2+L/R_3=(5*1024)/200+5/3+5/2=29.77≈30 секунд.}$$

<ins>Ответ:</ins> 30 секунд.
### Задание 3
Вероятность передачи данных 12 пользователями равна:

$$\{P=0.2^{n}=0.2^{12}≈4.1*10^{-9};}$$

где $\{n}$ - количество пользователей.

Такая вероятность пренебрежимо мала. С увеличением числа пользователей, вероятность уменьшается примерно в 10 раз. Поэтому можно считать это верхней границей для вероятности одновременной передачи данных 12 или более пользователями.

<ins>Ответ:</ins> $\{4.1*10^{-9}.}$
### Задание 4
Задержка первого пакета равна:

$$\{d=(80+S)/R=L/R}$$

Так как линии связи 3, то задержка $\{3*d}$. Каждый следующий пакет $\{X/S-1}$ тоже будет принимать другую задержку $\{d}$ - время, чтобы добраться от хоста А до хоста Б. Следовательно общая задержка для всех пакетов:

$$\{f(S):=d*(3+(X/S-1))=d*(X/S+2)=((80+S)/R)*(X/S+2);}$$

$$\{f(S)=80 * X / (R * S)+160/R+X/R+2*S/R.}$$

Найдем производную, чтобы найти минимальное значение:

$$\{f'(S)=(80 * X/R)(-1/S^2)+2*S/R=0;}$$

$$\{=>}$$

$$\{S=\sqrt{40*X}.}$$

При этом значении $\{S}$, $\{f"(S)>0}$, так что это локальный минимум.

<ins>Ответ:</ins> $\{S=\sqrt{40*X}.}$
### Задание 5
а) Задержка ожидания: $\{d_{ожид}=I * L / R(1-I)=a * L^2/(R * (R * (1-a * L / R)))=a * L^2/(R * (R-a * L));}$

Задержка передачи: $\{d_{перед}=L/R;}$

Общая задержка:

$$\{d_{общ}=d_{ожид}+d_{перед}=L/R+a * L^2/(R * (R-a * L))=L/(R-a*L);}$$

б) Для удобства заменим $\{x=L/R}$ 

$$\{d_{общ}(x)=L/R+a * L^2/(R * (R-a * L))=(L/R) * (1+a * L/(R-a * L)=}$$

$$\{x * (1+(L/R) * (a/(1-a * L/R))=x * (1+x  *(a/(1-a * x)).}$$

Чем-то отдалённо напоминает непрерывную дробь.

<ins>Ответ:</ins> а) $\{d_{общ}=L/(R-a*L);}$

б) $\{d_{общ}(x)=x * (1+x * (a / (1-a * x)).}$
