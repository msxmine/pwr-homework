import {categories} from "./values.js"

let myChart = null;
let myChartCat = null;

function initChart(){

    let profitChart = document.getElementById("profitsWeek")
    myChart = new Chart(profitChart, {
        type: 'line',
        data: {
        datasets: [{
            data: [],
            backgroundColor: [
                'rgb(0, 255, 0)'
            ],
            borderColor: [
                'rgb(0, 200, 0)'
            ]
        }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Przychód z ostatniego tygodnia"
                }
            }

        }
    })
    
    let categoryChart = document.getElementById("categoriesDay")
    myChartCat = new Chart(categoryChart, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
              label: 'Kategorie',
              data: [],
              hoverOffset: 4,
              backgroundColor: palette("mpn65", 50).map(function(hex) { return "#"+hex; })
            }]
          },
        options: {
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Tygodniowy przychód z kategorii"
                }
            }

        }
      });



    window.mcc = myChartCat
}

function drawCharts(sales){
    if (myChart == null){
        initChart();
    }

    let weeksal = parseSales(sales)
    let catsal = parseSalesCategories(sales);

    window.tytyty = catsal

    let labs = []
    let vals = []
    for (let cnam in catsal){
        labs.push(cnam);
        vals.push(catsal[cnam])
    }



    myChart.data.datasets[0].data = weeksal
    myChart.update()

    window.dba = myChartCat
    window.labs = labs
    window.vlss = vals

    myChartCat.data.labels = labs
    myChartCat.data.datasets[0].data = vals
    myChartCat.update();

}

function parseSales(sales){
    let dayssales = []
    let xsteps = []

    let startd = new Date()
    startd.setDate(startd.getDate()-6)

    for(let i = -6; i <= 0; i++){
        xsteps.push(startd.toDateString());
        dayssales.push(0);
        startd.setDate(startd.getDate()+1);
    }


    for (let saldat in sales){
        let datobj = new Date(parseInt(saldat))
        let xval = datobj.toDateString()
        let addr = xsteps.indexOf(xval)
        if (addr != -1){
            let sum = 0
            for (let prod in sales[saldat].soldProducts){
                let deets = sales[saldat].soldProducts[prod];
                sum += parseInt(deets.amount) * parseFloat(deets.price)
            }
            dayssales[addr] += sum
        }
    }

    let res = []
    for (let i = 0; i < 7; i++){
        res.push({x: xsteps[i], y: dayssales[i]})
    }

    return res
}

function parseSalesCategories(sales){
    let catsales = {}
    let startd = new Date()
    startd.setDate(startd.getDate() - 6)
    startd.setHours(0, 0, 0, 0)

    for (let saldat in sales){
        if (parseInt(saldat) > startd.getTime()){
            for (let prod in sales[saldat].soldProducts){
                let deets = sales[saldat].soldProducts[prod]
                let catgr = categories[parseInt(deets.category)]
                if (!(catgr in catsales)){
                    catsales[catgr] = 0
                }
                catsales[catgr] += parseInt(deets.amount) * parseFloat(deets.price)
            }
        }
    }

    return catsales
}

export {drawCharts}