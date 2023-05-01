## Homework 8. ***Транспортный уровень***

## 3. Задачи

### Задача 1

Средняя пропускная способность $\ { B }$ соединения определяется по формуле:

$$\ B = 1.22 * MSS / (RTT * \sqrt{L}). $$

Из этой формулы выведем частоту потерь $\ { L }$:

$$\ L = (1.22 * MSS / (RTT * B))^2. $$

TCP хост отправляет паследовательно пакеты объемом $\ { /L }$ (между потерявшимися). Тогда можно утверждать, что интервал времени $\ { T }$ можно записать как:

$$\ T = (1 / L) * MSS / B = MSS / (B * L); $$

Подставим в эту формулу выведенное значение $\ { L }$:

$$\ T = MSS / (B * (1.22 * MSS / (RTT * B))^2) = $$

$$\ = RTT^2 * B / (1.22^2 * MSS). $$

Как видно из полученной формулы, $\ { T }$ является функцией от средней пропускной способности ТСР, что и требовалось доказать.

### Задача 2

a. Для отправки и получения понадобится два $\ { RTT }$. В таком случае, общая задержка будет равна:

$$\ d = 2 * (S / R + RTT) + (4 + 8) * S / R + 2 * RTT = $$

$$\ = 2 * (S / R + RTT) + 12 * S / R + 2 * RTT = $$

$$\ = 4 * RTT + 14 * S / R; $$

Следовательно, время, необходимое для получения объекта составит: $\ 4 * RTT + 14 * S / R $.

б. Аналогично, для отправки и получения понадобится $\ { 2 * RTT }$. Тогда задержка:

$$\ d = 3 * (S / R + RTT) + 8 * S / R + 2 * RTT = $$

$$\ = 5 * RTT + 11 * S / R; $$

Время, необходимое для получения объекта составит: $\ 5 * RTT + 11 * S / R $.

в. Для отправки и получения понадобится $\ { 2 * RTT }$. Тогда задержка:

$$\ d = (S / R + RTT) + (8 + 4 + 2) * S / R + 2 * RTT = $$

$$\ = (S / R + RTT) + 14 * S / R + 2 * RTT =  $$

$$\ = 3 * RTT + 15 * S / R; $$

Время, необходимое для получения объекта составит: $\ 3 * RTT + 15 * S / R $.

### Задача 3

В модифицированном алгоритме размер окная увеличивается в $\ { (1 + a) }$ для каждого принятого ACK-пакета. Значит после получаения $\ { n }$ подтверждений размер окна перегрузки станет $\ W * (1 + a)^n $.

Время, необходимое для увеличения окна перегрузки с $\ { W / 2 }$ до $\ { W }$ можно записать как:

$$\ W = (W / 2) * (1 + a)^n. $$

Решая уравнение относительно $\ { n }$ получим:

$$\ n = log_2{(1 + a)}. $$

Это показывает, что количество подтверждений является постоянной величичной и зависит только от $\ { a }$.

Так как время от отправки пакета до получения подтверждения равен RTT, то время необходимое для увличения размера окна перегрузки также пропорциональна RTT. Следовательно, время также не зависит от средней пропускной способности TCP-соединения.

Теперь найдем зависимость между частой потерь $\ { L }$ и максимальным окном перегрузки $\ { W }$. В модифицированной алгоритме размер окна прегрузки уменьшается вдвое каждый раз, когда происходит потеря пакета. Следовательно, средний размер окна:

$$\ W_{ср} = (W + W / 2) / 2. $$

Частота потерь - количество потерянных пакетов в единицу времени:

$$\ L = 1 / (W_{ср} * RTT) = 1 / ((W + W / 2) / 2 * RTT) = $$

$$\ = 2 / (3 * W * RTT). $$

Из уравнения видно, что частота потерь обратно пропорциональна максимальному размеру окна перегрузки и RTT.

### Задача 4

Представим следующую временную диаграмму:

![plot](pictures/4.png)

Клиент отправляет запрос ближайшему серверу $\ { RTT_{FE} }$, который идёт за пакетами на дальний, что занимет 1 $\ { RTT_{BE} + ST }$ (где ST - время ожидания/задержки). Дальше клиенту остается только 3 $\ { RTT_{FE} }$ до ближнего сервиса:

$$\ 4 * RTT_{FE} + RTT_{BE} + ST. $$
