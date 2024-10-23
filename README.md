# rad-python-pr

Projeto da Disciplina - Sistema de Gerenciamento de Expedição Espacial

## Testando os Endpoints REST

os principais endpoints da API:

- Listar todas as missões (GET):

```
GET /missions
````

- Criar uma nova missão (POST):

```
POST /missions
```

### Payload (JSON):

```json
{
  "name": "Apollo 11",
  "launch_date": "1969-07-16",
  "destination": "Moon",
  "status": "Completed",
  "crew": "Neil Armstrong, Buzz Aldrin",
  "payload": "Lunar Module",
  "duration": "8 days",
  "cost": 1000000.0,
  "mission_status": "Successful"
}
```

- Visualizar uma missão específica (GET):
```
GET /missions/<int:mission_id>
```

- Atualizar uma missão específica (PUT):
```
PUT /missions/<int:mission_id>
```

- Excluir uma missão (DELETE):
```
DELETE /missions/<int:mission_id>
```

- Pesquisar missões por intervalo de datas (GET):
```
GET /missions/search?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```