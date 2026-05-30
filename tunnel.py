from pyngrok import ngrok

ngrok.set_auth_token("3ERx7kD4Fjj5c6FOrfB7xV8TaVH_5STQx8X9CNUBBiCQuMWVH")
public_url = ngrok.connect(8501)
print(public_url)