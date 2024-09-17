// Function to check if user is logged in
export const isLoggedIn = () => {
    const token = localStorage.getItem("authToken");
    return token !== null;
};
