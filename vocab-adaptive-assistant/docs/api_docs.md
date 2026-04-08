# API Documentation

## Health

- Method: `GET`
- Path: `/health`
- Response:

```json
{ "status": "ok" }
```

## Analyze Text

- Method: `POST`
- Path: `/analyze`
- Request:

```json
{
	"text": "The proliferation of complex systems can significantly impact learning outcomes."
}
```

- Response:

```json
{
	"level": "B2",
	"simplified_text": "The growth of complicated systems can greatly impact learning outcomes.",
	"difficult_words": [
		{
			"word": "proliferation",
			"meaning": "a rapid increase in number",
			"synonyms": ["growth", "expansion"]
		}
	]
}
```

