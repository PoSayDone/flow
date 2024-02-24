export function handle({event, resolve}) {
  const access_token = event.cookies.get('access_token')
  event.locals.is_authenticated = access_token ? true : false;

  return resolve(event)
}