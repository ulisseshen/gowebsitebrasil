<!--{
  "Title": "Avoiding SQL injection risk",
  "ia-translated": true
}-->

Você pode evitar um risco de SQL injection fornecendo valores de parâmetro SQL como argumentos de
função do package `sql`. Muitas funções no package `sql` fornecem
parâmetros para o statement SQL e para valores a serem usados nos parâmetros desse statement
(outras fornecem um parâmetro para um prepared statement e parâmetros).

O código no exemplo a seguir usa o símbolo `?` como um placeholder para o
parâmetro `id`, que é fornecido como um argumento de função:

```
// Correct format for executing an SQL statement with parameters.
rows, err := db.Query("SELECT * FROM user WHERE id = ?", id)
```

Funções do package `sql` que executam operações de banco de dados criam prepared
statements a partir dos argumentos que você fornece. Em tempo de execução, o package `sql` transforma
o statement SQL em um prepared statement e o envia junto com o
parâmetro, que é separado.

**Nota:** Placeholders de parâmetro variam dependendo do DBMS e driver
que você está usando. Por exemplo, o [driver pq](https://pkg.go.dev/github.com/lib/pq)
para Postgres aceita uma forma de placeholder como `$1` em vez de `?`.

Você pode ser tentado a usar uma função do package `fmt` para montar o
statement SQL como uma string com parâmetros incluídos – assim:

```
// SECURITY RISK!
rows, err := db.Query(fmt.Sprintf("SELECT * FROM user WHERE id = %s", id))
```

Isso não é seguro! Quando você faz isso, Go monta o statement SQL inteiro,
substituindo o verbo de formato `%s` com o valor do parâmetro, antes de enviar o
statement completo para o DBMS. Isso representa um
risco de [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) porque o
chamador do código poderia enviar um snippet SQL inesperado como o argumento `id`. Esse
snippet poderia completar o statement SQL de maneiras imprevisíveis que são
perigosas para sua aplicação.

Por exemplo, passando um certo valor `%s`, você pode acabar com algo
como o seguinte, que poderia retornar todos os registros de usuários no seu banco de dados:

```
SELECT * FROM user WHERE id = 1 OR 1=1;
```
