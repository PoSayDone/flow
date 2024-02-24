
<form method="POST" 
  use:enhance={() => {
    return async ({ result }) => {
      await invalidateAll();
      await applyAction(result);
    }
  }}
>
  <div>
    <label for="mail">mail</label>
    <input name="mail" required type="email" />
  </div>
  <div>
    <label for="password">Password</label>
    <input name="password" required type="password" />
  </div>
  <button>Login</button>
</form>