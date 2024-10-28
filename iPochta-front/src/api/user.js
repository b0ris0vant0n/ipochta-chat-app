export async function fetchUsername() {
    const email = localStorage.getItem('email');
  
    if (email) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/get_user?email=${encodeURIComponent(email)}`);
        const data = await response.json();
        
        if (data && data.length > 0) {
          console.log(data)
          return data;
        } else {
          console.error("Пользователь не найден");
          return null;
        }
      } catch (error) {
        console.error("Ошибка при получении имени пользователя:", error);
        return null;
      }
    } else {
      console.error("Email не найден в localStorage");
      return null;
    }
  }


  