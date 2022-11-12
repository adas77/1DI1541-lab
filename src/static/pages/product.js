const products = new Map()
const basket = new Map()

window.addEventListener('load', async () => {
    await fetch('/api/product/get')
        .then((response) => response.json())
        .then((data) => {
            data.forEach((u) => {
                products.set(u.product_id, { img: u.img, price: u.price, quantity: u.quantity })
                const img = `<img
        src="static/img/${u.img}"
        alt="${u.img}"
        onClick="imageClicked(${u.product_id})"
        width="400"
        height="341"
        title="${u.img}" />`
                const l = ` <tr>
              <td>${u.product_id}</td>
              <td>${img}</td>
              <td>${u.price}ZŁ/KG</td>
              <td>${u.quantity}</td>
              <td>${u.description}</td>
              <td>${u.reg_date}</td>
              <td><input id="product-${u.product_id}"  onkeydown="getQuantity(this,${u.product_id},${u.price})" type="number" placeholder="sztuk" ></td>
            </tr>`
                document.querySelector('table').insertAdjacentHTML('beforeend', l)
            })
        })
        .catch((err) => console.log(err))
})

const search = (val) => {
    const searchDiv = document.getElementById('search')
    while (searchDiv.firstChild) {
        searchDiv.removeChild(searchDiv.firstChild);
    }
    products.forEach((p, key) => {
        if (p.img.includes(val) && val.length > 0) {

            const img = `<img
        src="static/img/${p.img}"
        alt="${p.img}"
        onClick="imageClicked(${key})"
        width="80"
        height="70"
        title="${p.img}" />`
            searchDiv.insertAdjacentHTML('afterbegin', img)
        }
    });
}

const getQuantity = (quantity, product_id, price) => {
    quantity = quantity.value
    if (event.key === "Enter" && quantity > 0) {
        document.getElementById(`product-${product_id}`).value = '';
        const basketDiv = document.getElementById('basket')
        const basketSumDiv = document.getElementById('basket-sum')
        while (basketDiv.firstChild) {
            basketDiv.removeChild(basketDiv.firstChild);
        }
        basket.set(product_id, quantity)
        let sum = 0;
        basket.forEach((value, key) => {
            const product = products.get(key);
            const img = `<img
        src="static/img/${product.img}"
        alt="${product.img}"
        width="400"
        height="340"
        title="${product.img}" />`

            const be = ` <tr>
          <td>${key}</td>
          <td>${value}</td>
          <td>${product.price}</td>
          <td>${img}</td>
          <td><button onclick="deleteProduct(${key})">usun</button></td>
        </tr>`

            basketDiv.insertAdjacentHTML('beforeend', be)
            sum += product.price * value
        })
        basketSumDiv.innerHTML = sum
    }
}

const deleteProduct = (key) => {
    basket.delete(key)
}

const makeOrder = async () => {
    if (basket.size <= 0) { return }
    let p = "";
    basket.forEach((quantity, p_id) => {

        console.log(p_id)
        if (p) {
            p = p.concat(', ', p_id)
        }
        else {
            p = p.concat(p_id)
        }
    })

    const response = await fetch("api/order/create", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: `{
   "products_ids": [
    ${p}
]
  }`,
    });
    response.json().then((data) => {
        console.log(data);
        let sum = document.getElementById('basket-sum').innerHTML
        alert(`Your Order:\nid=${data.order_id}\nproducts=${p}\nprice:${sum}`);
        window.open(`/order`)
    });

}
const imageClicked = (product_id) => {
    window.open(`/api/product/get/${product_id}`)
}