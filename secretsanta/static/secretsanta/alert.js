function read(id){

	console.log('READ!!')
	console.log(id)
	fetch(`/read/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
        })
    return false;

}

