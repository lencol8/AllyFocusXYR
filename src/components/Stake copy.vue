<template>
  <div class="token">
        <div class="pop-up">
            <div class="black-container"></div>
            <div class="enable-dialog">
                <div class="dialog-title dialog-title--green">
                    <div class="close"></div>
                    <p>Enable</p>
                </div>
                <div class="text-container">To Stake LP tokens to the Cream Protocol, you need to enable it first.</div>
                <button class="dialog-button dialog-button--green">
                    <span>Enable</span>
                </button>
            </div>
        </div>
      <div class="block-reward">
          <div class="block-reward__container">
              <section class="reward">
                  <h1 class="reward__title">Reward</h1>
                  <div class="earned-container">
                      <div class="earned">
                          <h3 class="earned__title">Earned</h3>
                      </div>
                      <div class="container-reward">
                          <div class="balance-container">
                              <div class="white-container">
                                  <h3 class="white-container__title">C.R.E.A.M. Balance</h3>
                                  <p class="white-container__text">0.00000000</p>
                              </div>
                          </div>
                          <div class="earned-container">
                              <div class="white-container">
                                  <h3 class="white-container__title">C.R.E.A.M. Balance</h3>
                                  <p class="white-container__text">0.00000000</p>
                              </div>
                              <button class="earned-button" disabled="disabled">
                                  <span>Collect</span>
                              </button>
                          </div>
                      </div>
                  </div>
                  <div class="which-tokens-to-stake">
                      <h2 class="which-tokens-to-stake__title">Which tokens would you like to stake?</h2>
                      <div class="tab-container">
                          <div class="tab">
                              <h3 class="tab__title">Balancer</h3>
                          </div>
                          <div class="tab active">
                              <h3 class="tab__title">Uniswap</h3>
                          </div>
                          <div class="tab">
                              <h3 class="tab__title">C.R.E.A.M. Swap</h3>
                          </div>
                      </div>
                      <div class="stake-container">
                          <div class="stake-container__item">
                              <div class="stake-container__title stake-container__title--orange">
                                  <p class="stake-container__text stake-container__text--white">Stake</p>
                              </div>
                              <div class="white-container">
                                  <div class="balance-container">
                                      <div class="balance">Balance</div>
                                      <div class="amount-container">
                                          <div class="amount">0.000000</div>
                                          <div class="currency"></div>
                                      </div>
                                  </div>
                                  <div class="fill-amount">
                                      <div class="input-layout input-layout--big">
                                          <input type="number" placeholder="0" disabled="disabled">
                                      </div>
                                      <button class="input-btn input-btn--black" disabled="disabled">
                                          <span>Max</span>
                                      </button>
                                  </div>
                                  <button class="stake-button stake-button--orange">
                                      <span>Enable</span>
                                  </button>
                              </div>
                          </div>
                          <div class="stake-container__item">
                              <div class="stake-container__title">
                                  <p class="stake-container__text stake-container__text--white">Staked Balance</p>
                              </div>
                              <div class="white-container">
                                  <div class="balance-container">
                                      <div class="balance">Balance</div>
                                      <div class="amount-container">
                                          <div class="amount">0.000000</div>
                                          <div class="currency"></div>
                                      </div>
                                  </div>
                                  <div class="fill-amount">
                                      <div class="input-layout input-layout--big">
                                          <input type="number" placeholder="0" disabled="disabled">
                                      </div>
                                      <button class="input-btn input-btn--black" disabled="disabled">
                                          <span>Max</span>
                                      </button>
                                  </div>
                                  <button class="stake-button" disabled="disabled">
                                      <span>Unstake Tokens</span>
                                  </button>
                              </div>
                          </div>
                          <div class="stake-container__item">
                              <div class="stake-container__title stake-container__title--yellow">
                                  <p class="stake-container__text stake-container__text--white">Rewards Available</p>
                              </div>
                              <div class="white-container">
                                  <div class="balance-container">
                                      <div class="balance">Balance</div>
                                      <div class="amount-container">
                                          <div class="amount">0.000000</div>
                                          <div class="currency"></div>
                                      </div>
                                  </div>
                                  <button class="stake-button" disabled="disabled">
                                      <span>Claim Reward</span>
                                  </button>
                              </div>
                          </div>
                      </div>
                      <div>
                          <button class="claim-and-unstake clain-and-unstake--green" disabled="disabled">
                              <span>Exit : Claim and Unstake</span>
                          </button>
                      </div>
                      <div class="stake-info-link">
                          <a href="" class="stake-info-link__link" target="_blank">Balancer: CREAM/ETH 80/20</a>
                          <p class="stake-info-link__delim">,</p>
                          <a href="" class="stake-info-link__link" target="_blank">Uniswap: CREAM/ETH 50/50</a>
                      </div>
                  </div>
              </section>
          </div>
      </div>
  </div>
</template>

<script>

export default {
  name: "Stake",
  data() {
    return {
    };
  },
  watch: {
  },
  computed: {
  },
  methods: {

  },
  mounted() {

  },
  beforeDestroy() {

  },
};
</script>

<style scoped>

.pop-up {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1002;
}

.pop-up .black-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,.4);
}

.enable-dialog {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    width: 600px;
    background-color: #fff;
    border: 6px solid #000;
}

.dialog-title {
    position: relative;
    background-color: #ffb8d2;
    padding: 15px;
    border-bottom: 6px solid #000;
}

.dialog-title--green {
    background-color: #69e2dc;
}

.dialog-title .close {
    position: absolute;
    top: 20px;
    right: 20px;
    height: 24px;
    width: 24px;
    background-repeat: no-repeat;
    background-size: contain;
    background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTE4IDZMNiAxOE02IDZsMTIgMTIiIHN0cm9rZT0iIzAwMCIgc3Ryb2tlLXdpZHRoPSI0IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=);
    cursor: pointer;
}

.dialog-title p {
    font-family: "Muli";
    text-align: center;
    font-size: 36px;
    color: #000;
    font-weight: 700;
    padding: 0 26px;
    margin: 0;
}

.enable-dialog .text-container {
    padding: 20px;
    font-weight: 700;
    font-size: 20px;
    line-height: 28px;
    text-align: center;
}

.dialog-button {
    width: 100%;
    height: 100%;
    border: 6px solid #000;
    cursor: pointer;
    font-size: 22px;
    background-color: #ff6583;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: .3s;
    font-weight: 700;
}

.dialog-button--green{
    background-color: #65d9d3;
}

.enable-dialog .dialog-button {
    width: 404px;
    height: 60px;
    margin: 40px auto 16px;
}

.dialog-button span {
    color: #000;
    transition: all 0.3s;
}

.dialog-button:hover span {
    color: #fff;
}

@media (max-width: 767px) {
    .enable-dialog {
        width: calc(100% - 20px);
    }
}

@media (max-width: 575px) {
    .enable-dialog .dialog-button {
        width: 280px;
    }
}

</style>

<style scoped>

@font-face {
    font-family: '04B_19__';
    src: url(../assets/fonts/04B_19__.eot) format('embedded-opentype');
    src: url(../assets/fonts/04B_19__.woff2) format('woff2');
    src: url(../assets/fonts/04B_19__.woff) format('woff');
    font-style: normal;
    font-weight: normal;
}

@font-face {
    font-family: 'Muli';
    src: url(../assets/fonts/Muli.eot) format('embedded-opentype');
    src: url(../assets/fonts/Muli.woff2) format('woff2');
    src: url(../assets/fonts/Muli.woff) format('woff');
    font-style: normal;
    font-weight: normal;
}

.block-reward {
    width: 100%;
    height: 100%;
    padding: 20px 0;
    display: flex;
    min-height: calc(100vh - 138px);
}

.block-reward__container {
    width: 100%;
    background-color: #cdc5ff;
    padding: 50px;
    margin: 0;
    border-radius: 20px;
}

.reward {
    color: #000;
}

.reward p {
    margin-bottom: 0;
}

.reward__title {
    font-family: "04B_19__";
    text-align: center;
    color: #fff;
    font-size: 56px;
    line-height: 56px;
    margin: 2px auto 20px;
    -webkit-text-stroke: 3px #000;
}

.earned-container {
    display: flex;
    margin-bottom: 20px;
    height: 140px;
}

.earned-container .earned {
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding: 0 53px;
    border: 6px solid #000;
    background-color: #f4db62;
}

.earned-container .container-reward {
    width: 100%;
}

.earned-container .balance-container,
.earned-container .earned-container {
    height: 50%;
}

.earned .earned__title {
    font-family: "04B_19__";
    font-size: 30px;
    color: #f4db62;
    -webkit-text-stroke: 3px #000;
    text-shadow: 0 5px 1px rgba(0,0,0,.3);
}

.earned-container .balance-container .white-container,
.earned-container .earned-container .white-container {
    border-left: 0;
}

.earned-container .earned-container .white-container {
    border-right: 0;
}

.earned-container .white-container {
    display: flex;
    width: 100%;
    background-color: #fff;
    border: 6px solid #000;
    padding: 17px;
}

.earned-container .container-reward .white-container__title,
.earned-container .container-reward .white-container__text {
    align-self: center;
}

.earned-container .container-reward .white-container__title {
    font-family: "Muli";
    font-weight: 700;
    font-size: 18px;
    line-height: 20px;
    margin-right: 20px;
    width: 163px;
}

.earned-container .container-reward .white-container__text {
    margin-bottom: 0;
    font-family: "Muli";
    font-weight: 700;
    font-size: 30px;
    line-height: 30px;
    letter-spacing: .01em;
}

.earned-container .earned-container .earned-button {
    width: 201px;
}

.earned-button[disabled] {
    background-color: #848484;
}

.earned-button.yellow {
    background-color: #ffce00;
}

.earned-button {
    width: 100%;
    height: 100%;
    border: 6px solid #000;
    cursor: pointer;
    font-size: 22px;
    background-color: #ff6583;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: .3s;
    font-weight: 700;
}

.earned-button[disabled] span {
    color: #000;
}

.earned-button span {
    transition: .3s;
}

section.reward .which-tokens-to-stake {
    background-color: #fff;
    padding: 36px 27px 27px;
    border: 6px solid #000;
}

.which-tokens-to-stake__title {
    font-family: "04B_19__";
    text-align: center;
    color: #fff;
    font-size: 45px;
    line-height: 45px;
    -webkit-text-stroke: 3px #000;
    margin-bottom: 28px;
}

.tab-container {
    display: flex;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.tab-container .tab {
    position: relative;
    width: 33.33%;
    display: flex;
    justify-content: center;
    background-color: #fff;
    padding: 13px;
    border: 6px solid #000;
    cursor: pointer;
}

.tab-container .tab:first-child {
    border-right: 0;
}

.tab-container .tab:last-child {
    border-left: 0;
}

.tab-container .tab.active,
.tab-container .tab:hover {
    background-color: #69e2dc;
}

.tab-container .tab .tab__title {
    font-family: "Muli";
    font-weight: "bold";
    font-size: 26px;
    line-height: 30px;
    text-align: center;
}

.tab-container .tab .tab__title,
.tab-container .tab .tab p {
    position: relative;
    align-self: center;
    z-index: 1;
}

.stake-container {
    display: flex;
}

.stake-container .stake-container__item {
    flex: 1;
    margin-right: 20px;
}

.stake-container .stake-container__item:last-child {
    margin-right: 0;
}

.stake-container__title {
    width: 100%;
    border: 6px solid #000;
    padding: 33px;
    background-color: #ffb8d2;
}

.stake-container__title--orange {
    background-color: #ffc78a;
}

.stake-container__title--yellow {
    background-color: #f4db62;
}

.stake-container__text {
    text-align: center;
    font-family: "04B_19__";
    font-size: 30px;
    color: #ffb8d2;
    -webkit-text-stroke: 3px #000;
    text-shadow: 0 5px 1px rgba(0,0,0,.3);
}

.stake-container__text--white {
    color: #fff;
    text-shadow: none;
}

.stake-container .stake-container__item .white-container {
    border: 6px solid #000;
    border-top: 0;
    padding: 31px 22px 18px;
}

.stake-container .stake-container__item .white-container .balance-container .balance {
    font-family: "Muli";
    font-weight: 700;
    font-size: 18px;
    text-align: left;
    margin-bottom: 5px;
}

.stake-container .stake-container__item .white-container .balance-container .amount-container {
    display: flex;
    margin-bottom: 18px;
}

.stake-container .stake-container__item .white-container .balance-container .amount-container .amount,
.stake-container .stake-container__item .white-container .balance-container .amount-container .currency {
    align-self: center;
    font-family: "Muli";
    font-weight: 700;
}

.stake-container .stake-container__item .white-container .balance-container .amount-container .amount {
    font-size: 24px;
    margin-right: 10px;
    word-break: break-word;
}

.stake-container .stake-container__item .white-container .balance-container .amount-container .currency {
    font-size: 16px;
    margin-left: auto;
}

.stake-button {
    width: 100%;
    height: 100%;
    border: 6px solid #000;
    cursor: pointer;
    font-size: 22px;
    background-color: #ff6583;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: .3s;
    font-weight: 700;
}

.stake-button--orange {
    background-color: #ff7816;
}

.stake-container .stake-container__item .white-container > .stake-button {
    display: block;
    height: 60px;
    margin-top: 20px;
}

.stake-button span {
    transition: .3s;
}

.stake-container .stake-container__item .white-container .fill-amount {
    display: flex;
    justify-content: center;
    height: 76px;
}

.stake-container .stake-container__item .white-container .fill-amount .input-layout {
    width: 100%;
    border: 6px solid #000;
    border-right: 0;
}

.input-layout input {
    font-family: "Muli";
    background-color: inherit;
    color: inherit;
    -webkit-text-fill-color: inherit;
    cursor: inherit;
    font-size: 16px;
    line-height: 1.29;
    padding: 0;
    margin: 0;
    overflow: hidden;
    appearance: textfield;
}

.input-layout input:disabled {
    background-color: #c4c4c4;
}

.stake-container .stake-container__item .white-container .fill-amount .input-layout input {
    width: 100%;
    height: 100%;
    font-size: 30px;
    border: 0;
    padding: 20px;
}

.stake-container .stake-container__item .white-container .fill-amount .input-layout--big input {
    font-size: 30px;
}

.input-btn {
    width: 100%;
    height: 100%;
    border: 6px solid #000;
    cursor: pointer;
    font-size: 22px;
    background-color: #ff6583;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: .3s;
    font-weight: 700;
}

.input-btn--black {
    background-color: #000;
}

.stake-button[disabled],
.input-btn[disabled] {
    background-color: #848484;
    cursor: not-allowed;
    pointer-events: none;
}

.stake-container .stake-container__item .white-container .fill-amount .input-btn--black {
    width: 61px;
    height: 100%;
}

.input-btn[disabled] span {
    color: #000;
    transition: .3s;
}

.input-btn--black span,
.input-btn:hover span {
    color: #fff;
}

@media (max-width: 1510px) {
    .stake-container .container__item .stake-container__title {
        height: 138px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}

.claim-and-unstake {
    display: block;
    min-height: 60px;
    margin-top: 20px;
    width: 100%;
    height: 100%;
    border: 6px solid #000;
    cursor: pointer;
    font-size: 22px;
    background-color: #ff6583;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: .3s;
    font-weight: 700;
}

.clain-and-unstake--green {
    background-color: #65d9d3;
}

.claim-and-unstake[disabled] {
    background-color: #848484;
}

.claim-and-unstake[disabled] span {
    color: #000;
}

.claim-and-unstake span {
    transition: .3s;
}

.stake-info-link {
    display: flex;
    justify-content: center;
    margin-top: 25px;
}

.stake-info-link__link {
    font-size: 16px;
    color: #6d6d6d;
    text-decoration: underline;
}

.stake-info-link__link:hover {
    color: #c4c4c4;
}

.stake-info-link__delim {
    font-size: 16px;
    color: #6d6d6d;
    margin: 0 2.5px;
}

@media (max-width: 1439px) {
    .stake-container {
        flex-direction: column;
    }
    .stake-container .stake-container__item {
        margin: 0 0 20px;
    }
}

@media (max-width: 991px) {
    .earned-container {
        height: auto;
        flex-direction: column;
    }
    .container {
        width: 100%;
    }
    .earned-container .earned-container {
        margin-bottom: 0;
    }
    .earned-container .earned-container .white-container {
        border-right: 6px solid #000;
    }
    .earned-container .balance-container .white-container,
    .earned-container .earned-container .white-container {
        border-top: 0;
        border-left: 6px solid #000;
    }
    .earned-container .earned-container .earned-button {
        width: 100%;
        height: 50px;
        border-top: 0;
    }
}

@media (max-width: 991px) {
    .stake-info-link {
        flex-direction: column;
        align-items: center;
    }
    .stake-info-link__link {
        margin: 10px;
    }
    .stake-info-link__delim {
        display: none;
    }
}

@media (max-width: 767px) {
    .block-reward .block-reward__container {
        padding: 15px
    }
    .tab-container .tab {
        width: 50%;
        border: 4px solid #000;
    }
    .tab-container .tab:last-child {
        width: 100%;
        border: 4px solid #000;
        border-top: 0;
    }
    .earned-container .white-container {
        flex-direction: column;
    }
    .earned-container .white-container .white-container__title {
        margin-right: 0;
        margin-bottom: 6px;
        width: 100%;
    }
}

@media (max-width: 575px) {
    .which-tokens-to-stake .which-tokens-to-stake__title {
        font-size: 30px;
        line-height: 30px;
        -webkit-text-stroke: 2px #000;
        margin-bottom: 20px;
    }
    .tab-container .tab .tab__title {
        font-size: 16px;
    }
    .stake-button,
    .input-btn {
        font-size: 16px;
    }
    .stake-container .stake-container__item .white-container .fill-amount .input-layout--big input{
        font-size: 20px;
    }
    .stake-container .stake-container__item .white-container .fill-amount .input-btn--black {
        width: 76px;
    }
    .claim-and-unstake {
        font-size: 15px;
    }
    .stake-info-link__link {
        font-size: 14px;
    }
}

</style>