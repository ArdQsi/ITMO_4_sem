/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "i2c.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "kb.h"
#include "sdk_uart.h"
#include "pca9538.h"
#include "oled.h"
#include "fonts.h"
#include <string.h>
#include <stdlib.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */
void KB_Test( void );
void OLED_KB( uint8_t OLED_Keys[]);
void oled_Reset( void );
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
int previous_len = 0;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */
  

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_I2C1_Init();
  MX_USART6_UART_Init();
  /* USER CODE BEGIN 2 */
  oled_Init();

  /* USER CODE END 2 */
 
 

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  KB_Test();
	  HAL_Delay(500);

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage 
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 25;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

int isOperation(char c) {
	return (c == '+' || c == '-' || c =='*');
}

int priority(char operation) {
    switch (operation) {
    case '+':
    case '-':
        return 1;

    case '*':
        return 2;
    }

    return 0;
}

int kurwa(char * linia)
{
    int MAX_SIZE = 128;

    char *token = strtok(linia, " ");

    char *operations[MAX_SIZE];
    char *output[MAX_SIZE * 2];

    int out_counter = 0, op_counter = 0;

    while (token != NULL)
    {
        if (strlen(token) > 1 || isdigit(token[0]))
            output[out_counter++] = token;
        else
        {
            if (op_counter == 0)
                operations[op_counter++] = token;
            else if (priority(*operations[op_counter - 1]) >= priority(*token))
            {
                output[out_counter++] = operations[op_counter - 1];
                operations[op_counter - 1] = token;
            }
            else
                operations[op_counter++] = token;
        }

        token = strtok(NULL, " ");
    }

    op_counter -= 1;

    while (op_counter >= 0)
    {
        output[out_counter++] = operations[op_counter--];
    }

    int numbers[MAX_SIZE];
    int num_counter = 0;
    int variable;
    int overflow = 0;

    for (int i = 0; i < out_counter; i++)
    {
        if (strlen(output[i]) > 1 || isdigit(output[i][0]))
            numbers[num_counter++] = atoi(output[i]);
        else
        {
            switch (output[i][0])
            {
            case '-':
            {
                variable = -numbers[--num_counter];
                variable += numbers[--num_counter];

                numbers[num_counter++] = variable;

                break;
            }

            case '+':
                variable = numbers[--num_counter];
                variable += numbers[--num_counter];
                numbers[num_counter++] = variable;

                break;
            case '*':
                variable = numbers[--num_counter];
                variable *= numbers[--num_counter];
                numbers[num_counter++] = variable;

                break;
            default:
                break;
            }
        }
    }

    return numbers[--num_counter];
}

void KB_Test( void ) {
	UART_Transmit( (uint8_t*)"KB test start\n" );
	uint8_t Row[4] = {ROW4, ROW3, ROW2, ROW1}, Key, OLED_Keys[12] = {0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30,0x30};
	oled_Reset();
	custom_hello_world("Hello world!");
	oled_UpdateScreen();
	int isEnter = 0, isShift = 0;
	char input_string[128];
	input_string[0] = '\0';
	int input_counter = 0;
	while(isEnter == 0) {
		for ( int i = 0; i < 4; i++ ) {
			Key = Check_Row( Row[i] );
			switch(Key) {
				case 0x01:
					if (isShift == 1) {
						if(input_counter != 0) {
							if (isOperation(input_string[input_counter - 2]))
								input_string[input_counter  - 2] = '+';
							else {
								strcat(input_string, " + ");
								input_counter += 3;
							}
							custom_oled_kb(input_string);
						}
					} else {
						strcat(input_string, "1");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x02:
					if (isShift == 1) {
						if (input_counter != 0) {
							if (isOperation(input_string[input_counter - 2]))
								input_string[input_counter - 2] = '-';
							else {
								strcat(input_string, " - ");
								input_counter += 3;
							}
							custom_oled_kb(input_string);
						}
					} else {
						strcat(input_string, "2");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x03:
					if (isShift == 1) {
						if (input_counter != 0) {
							if (isOperation(input_string[input_counter - 2]))
								input_string[input_counter - 2] = '*';
							else {
								strcat(input_string, " * ");
								input_counter += 3;
							}
							custom_oled_kb(input_string);
						}
					} else {
						strcat(input_string, "3");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x04:
					if (isShift == 0) {
						strcat(input_string, "4");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x05:
					if (isShift == 0) {
						strcat(input_string, "5");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x06:
					if (isShift == 0) {
						strcat(input_string, "6");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x07:
					if (isShift == 0) {
						strcat(input_string, "7");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x08:
					if (isShift == 0) {
						strcat(input_string, "8");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x09:
					if (isShift == 0) {
						strcat(input_string, "9");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x0A:
					isShift = 1;
					break;
				case 0x0B:
					if (isShift == 0) {
						strcat(input_string, "0");
						custom_oled_kb(input_string);
						input_counter++;
					}
					isShift = 0;
					break;
				case 0x0C: ;
					if (isShift == 0) {
						if (isOperation(input_string[input_counter - 2])) break;
						char new_string[32];
						itoa(kurwa(input_string), new_string, 10);
						input_string[0] = '\0';
						strcat(input_string, new_string);
						custom_oled_kb(input_string);
						isShift = 0;
						input_counter = strlen(new_string);
					} else {
						input_string[0] = '\0';
						isShift = 0;
						input_counter = 0;
						oled_Reset();
					}
					break;
				default:
					break;
			}
			HAL_Delay(25);
		}

	}
	UART_Transmit( (uint8_t*)"KB test complete\n");
}
void OLED_KB( uint8_t OLED_Keys[12]) {
	for (int i = 3; i >= 0; i--) {
		oled_SetCursor(56, 5+(4-i)*10);
		for (int j = 0; j < 3; j++) {
			oled_WriteChar(OLED_Keys[j+3*i], Font_7x10, White);
		}
	}
	oled_UpdateScreen();
}

void custom_oled_kb(char *line) {
	oled_Reset();
	int current_line = 0;
	int current_x = 1;
	for (int i = 0; i < strlen(line); i++) {
		if (i != 0 && i % 18 == 0) current_line++;
		oled_SetCursor(current_x, 10 * current_line);
		current_x += 7;
		if (current_x == 127) current_x = 1;
		oled_WriteChar(line[i], Font_7x10, White);
	}
	oled_UpdateScreen();
}

void oled_Reset( void ) {
	oled_Fill(Black);
	oled_SetCursor(0, 0);
	oled_UpdateScreen();
}

void custom_hello_world(char* line) {
	oled_Reset();
		int current_x = (64 - (strlen(line))) / 2;
		for (int i = 0; i < strlen(line); i++) {
			oled_SetCursor(current_x, 25);
			current_x += 7;
			oled_WriteChar(line[i], Font_7x10, White);
		}
		oled_UpdateScreen();
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
