const products = new Map()
const basket = new Map()

window.addEventListener('load', () => {
    // basket.forEach(b => {
    //     console.log(b)
    // })

    fetch('/api/product/get')
        .then((response) => response.json())
        .then((data) => {
            data.forEach((u) => {
                products.set(u.product_id, { img: u.img, price: u.price, quantity: u.quantity })
                // console.log(products)
                const img = `<img
        src="static/img/${u.img}"
        alt="${u.img}"
        onClick="imageClicked(${u.product_id})"
        width="400"
        height="341"
        title="${u.img}" />`

                //<img src="{{ url_for('static', filename = 'japko.jpg') }}" align="middle" />
                const l = ` <tr>
              <td>${u.product_id}</td>
              <td>${img}</td>
              <td>${u.price}ZŁ/KG</td>
              <td>${u.quantity}</td>
              <td>${u.description}</td>
              <td>${u.reg_date}</td>
              <td><input  onkeydown="getQuantity(this.value,${u.product_id},${u.price})" type="number" placeholder="sztuk" value=0></td>
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
            console.log(p)

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

const handleButton = ($this) => {
    letval = $this.previousElementSibling.value;

    console.log("button pressed")
    if (val == '') {
        console.log('no input');
    } else {
        console.log(val);
    }
};

const getQuantity = (quantity, product_id, price) => {
    if (event.key === "Enter" && quantity > 0) {
        const basketDiv = document.getElementById('basket')
        const basketSumDiv = document.getElementById('basket-sum')
        while (basketDiv.firstChild) {
            basketDiv.removeChild(basketDiv.firstChild);
        }

        basket.set(product_id, quantity)
        //const product = products.get(product_id);
        //console.log(`product:${product.}`)

        let sum = 0;
        basket.forEach((value, key) => {
            const product = products.get(key);

            const img = `<img
        src="static/img/${product.img}"
        alt="${product.img}"
        width="400"
        height="341"
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
    console.log("fff")
    console.log(basket)
    basket.delete(key)
    console.log(basket)

}

const makeOrder = async () => {
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

        //   body: `{
        //     "user_id": ${1},
        //     "products_ids": [
        //      ${p}
        //  ]
        //    }`,
    });

    response.json().then(data => {
        console.log(data);
    });
}

const imageClicked = (product_id) => {
    window.open(`/api/product/get/${product_id}`)
}


