# MachineLearning_Task2
Дана матрица рейтингов User-Item, по кросс-валидации бьем её на фолды, затем пытаемся предсказать скрытые рейтинги. Качество проверяем по RMSE, только для тех точек в которых прогноз есть.
 
Используем факторизационную машину 2-го порядка с квадратичной функцией потерь (аналогично линейной регрессии).

Датасет: https://www.kaggle.com/netflix-inc/netflix-prize-data/data#combined_data_1.txt 

## Результат

### Train Fold 0
Test fold 1

RMSE 1.1491350584991595

Test fold 2

RMSE 1.1545439813819531

Test fold 3

RMSE 1.15364404131489

### Train Fold 1
Test fold 0

RMSE 1.1487569395588155

Test fold 2

RMSE 1.1539784975566614

Test fold 3

RMSE 1.153180552736331

### Train Fold 2

Test fold 0

RMSE 1.1403261226501233

Test fold 1

RMSE 1.1411291972313366

Test fold 3

RMSE 1.1417062321001476

### Train Fold 3

Test fold 0

RMSE 1.1406067891509188

Test fold 1

RMSE 1.1414010762965455

Test fold 2

RMSE 1.1428708433010738
