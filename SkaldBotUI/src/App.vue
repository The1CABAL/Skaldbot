<template>
    <div id="app">
        <div class="container">
            <div class="logo">
                <img :src="logoImage" style="height: 60px;"/>
            </div>
            <div class="navbar">
                <div class="icon-bar" @click="Show()">
                    <i></i>
                    <i></i>
                    <i></i>
                </div>
                <ul id="nav-lists">
                    <li class="close"><span @click="Hide()">&times;</span></li>
                    <li><router-link to="/">Home</router-link></li>
                    <li><router-link to="/about">About</router-link></li>
                    <li><router-link to="/suggestions">Submit Ideas</router-link></li>
                </ul>
            </div>
        </div>
        <router-view></router-view>
    </div>
</template>

<script>
    export default {
        name: "app",
        data() {
            return {
                logoImage: require('@/assets/logo.png'),
                background: require('@/assets/SbBackground.jpg')
            }
        },
        methods: {
            Show() {
                document.getElementById("nav-lists").classList.add("_Menus-show");
            },
            Hide() {
                document.getElementById("nav-lists").classList.remove("_Menus-show");
            }
        }
    }
</script>

<style>
    *,
    *::before,
    *::after {
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
    }

    .container {
        height: 60px;
        background-color: #479194;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        overflow: hidden;
    }

        .container .logo {
            max-width: 250px;
            padding: 0 10px;
            overflow: hidden;
            max-height: 60px;
        }

            .container .logo a {
                display: -webkit-box;
                display: -ms-flexbox;
                display: flex;
                -ms-flex-wrap: wrap;
                flex-wrap: wrap;
                -webkit-box-align: center;
                -ms-flex-align: center;
                align-items: center;
                height: 60px;
            }

                .container .logo a img {
                    max-width: 100%;
                    max-height: 60px;
                }

        .container .navbar {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -ms-flex-wrap: wrap;
            flex-wrap: wrap;
            -webkit-box-flex: 1;
            -ms-flex: 1;
            flex: 1;
            padding: 0 5px;
        }

            .container .navbar ul {
                display: -webkit-box;
                display: -ms-flexbox;
                display: flex;
                -ms-flex-wrap: wrap;
                flex-wrap: wrap;
                list-style: none;
                margin: 0;
                padding: 0;
            }

                .container .navbar ul li a {
                    text-decoration: none;
                    color: #fff;
                    font-size: 14px;
                    text-transform: uppercase;
                    display: block;
                    height: 60px;
                    line-height: 60px;
                    cursor: pointer;
                    padding: 0 10px;
                }

                    .container .navbar ul li a:hover {
                        color: #ffffff;
                        background-color: #3D8083;
                    }

                .container .navbar ul .close {
                    display: none;
                    text-align: right;
                    padding: 10px;
                }

                    .container .navbar ul .close span {
                        font-size: 40px;
                        display: inline-block;
                        padding: 0 10px;
                        cursor: pointer;
                    }

            .container .navbar .icon-bar {
                padding: 18px 8px;
                width: 50px;
                height: 60px;
                display: none;
                -webkit-box-orient: vertical;
                -webkit-box-direction: normal;
                -ms-flex-direction: column;
                flex-direction: column;
                -webkit-box-pack: justify;
                -ms-flex-pack: justify;
                justify-content: space-between;
                cursor: pointer;
            }

                .container .navbar .icon-bar i {
                    background-color: #ffffff;
                    height: 2px;
                }

    @media only screen and (max-width: 650px) {
        .container {
            -webkit-box-pack: justify;
            -ms-flex-pack: justify;
            justify-content: space-between;
        }

            .container .logo {
                -webkit-box-flex: 1;
                -ms-flex: 1;
                flex: 1;
            }

            .container .navbar {
                -webkit-box-flex: 0;
                -ms-flex: 0;
                flex: 0;
            }

                .container .navbar ul {
                    -ms-flex-wrap: nowrap;
                    flex-wrap: nowrap;
                    position: fixed;
                    left: 100%;
                    -webkit-box-orient: vertical;
                    -webkit-box-direction: normal;
                    -ms-flex-direction: column;
                    flex-direction: column;
                    background: #ffffff;
                    width: 100%;
                    height: 100%;
                    overflow: auto;
                    -webkit-transition: left .3s;
                    -o-transition: left .3s;
                    transition: left .3s;
                }

                    .container .navbar ul li a {
                        padding: 10px;
                        font-size: 16px;
                        height: auto;
                        line-height: normal;
                        color: #555555;
                    }

                    .container .navbar ul .close {
                        display: block;
                    }

                .container .navbar .icon-bar {
                    display: -webkit-box;
                    display: -ms-flexbox;
                    display: flex;
                }

                .container .navbar ._Menus-show {
                    left: 0;
                }
    }
    .titleLink {
        text-decoration: none;
        color: white;
        font-size: 20px;
    }

    .activeLink {
        background-color: #59ACAF;
    }

    body {
        background-color: #C9C9C9;
    }
</style>