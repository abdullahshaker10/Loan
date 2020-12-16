function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
class Offer {
  constructor(offer) {
    this.offer = offer;
    this.offerId = offer.data("offer");
    this.acceptRow = this.offer.find(".accept");
    this.acceptButton = this.offer.find(".acceptOffer ");
    this.pay = this.offer.find(".pay");
    this.pay.on("click", this.handelPay);
    this.acceptButton.on("click", this.handelAccept);
    console.log(this.offerId);
  }

  updateLoan = (state, loanId) => {
    let url = `/api/loan/${loanId}`;

    fetch(url, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "PATCH",
      body: JSON.stringify({ state: state }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("data is", data);
      });
  };
  updateOffer = (state) => {
    let url = `/api/offer/${this.offerId}`;
    let currentDate = new Date();
    currentDate = currentDate.getTime() / 1000;
    fetch(url, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "PATCH",
      body: JSON.stringify({ state: state, date: currentDate }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("data is", data);
        let loanId = data.loan.id;
        console.log("loan Id is ", loanId);
        if (state === "Funded" || state === "Completed") {
          let stateTemp = `<td class="state">${state}</td>`;
          this.offer.find(".state").replaceWith(stateTemp);
          this.updateLoan(state, loanId);
          if (!alert(`Loan ${state}`)) {
            window.location.reload();
          }
        } else if (data.rest_paymrnts === 0) {
          this.updateOffer("Completed");
        } else if (state == "Paying") {
          console.log("ok");
          let temp = `<td class="rem">Remaining ${data.rest_paymrnts} payments</td>`;
          this.offer.find(".rem").replaceWith(temp);
        }
      });
  };
  handelAccept = () => {
    this.updateOffer("Funded");

    this.offer.find(".acceptOffer").remove();
    console.log("accept clicked");
  };

  handelPay = () => {
    console.log("pay clicked");
    this.updateOffer("Paying");
    let stateTemp = `<td class="state">Paying</td>`;
    this.offer.find(".state").replaceWith(stateTemp);
  };
}

$(".offer").each(function () {
  let new_offer = new Offer($(this));
});
