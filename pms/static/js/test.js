const getName = new Promise((resolve, reject) => {
    setTimeout(() => {
        reject("My Name is Omojugba Olawale Festus");
    }, 5000);
});

getName
.then(ids => {
    console.log(ids);
})
.catch(error =>{
    console.log("An Error Occur")
})