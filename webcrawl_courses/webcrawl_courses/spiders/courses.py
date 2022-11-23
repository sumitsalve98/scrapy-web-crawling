import scrapy
from ..items import WebcrawlCoursesItem


class course_crawler(scrapy.Spider):
    name = "course_crawler"

    start_urls = [
        "https://talentedge.com/iit-delhi/operations-management-and-analytics-course",
        "https://talentedge.com/xlri-jamshedpur/financial-management-course",
        "https://talentedge.com/xlri-jamshedpur/human-resource-management-course",
        "https://talentedge.com/iim-kozhikode/professional-certificate-program-marketing-sales-management-iim-kozhikode",
        "https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics"

    ]
    def parse(self, response, **kwargs):
        courses = WebcrawlCoursesItem()


        try:
            #scraping title

            Title = response.xpath("//*[@id='app']/section[1]/div/div/div/div/div[1]/div/div/div[2]/h1/text()").extract()
            Bold_Title = response.xpath("//*[@id='app']/section[1]/div/div/div/div/div[1]/div/div/div[2]/h1/b/text()").extract()
            Full_Title_list = []
            Full_Title_list.extend(Title)
            Full_Title_list.extend(Bold_Title)
            Full_Title_text = ""
            for line in Full_Title_list:
                Full_Title_text = Full_Title_text + line
            Full_Title_text = Full_Title_text.strip().replace("  " , " ")
            print(Full_Title_text)

        except Exception as e:
            print(f"Error while scraping Title: {e}")



        try:
            # scraping short description

            Short_Description1 = response.xpath("//*[@id='app']/section[1]/div/div/div/div/div[1]/div/div/div[2]/p/text()").extract()
            Short_Description2 = response.xpath("//*[@id='app']/section[1]/div/div/div/div/div[1]/div/div/div[2]/div/p/span/text()").extract()

            Full_Short_Description_list = []
            Full_Short_Description_list.extend(Short_Description1)
            Full_Short_Description_list.extend(Short_Description2)

            Full_Short_Description_string = ""
            for line in Full_Short_Description_list:
                Full_Short_Description_string = Full_Short_Description_string + line +", "
            Full_Short_Description_string = Full_Short_Description_string[:-2].replace("  "," ").strip()
            print(Full_Short_Description_string)

        except Exception as e:
            print(f"Error while scraping short description: {e}")



        try:
            # scraping description

            Description_para1 = response.xpath("//*[@id='doverview']/div/div/div[1]/div[1]/div/div[1]/p[1]/strong/text()").extract()
            Description_para2 = response.xpath("//*[@id='doverview']/div/div/div[1]/div[1]/div/div[1]/p/text()").extract()

            Description_para = []
            Description_para.extend(Description_para1)
            Description_para.extend(Description_para2)

            Description_para_string = ""
            for para in Description_para:
                Description_para_string = Description_para_string + para + "\n\n"
            Description_para_string = Description_para_string.replace("  "," ")[:-2]
            print(Description_para_string)

        except Exception as e:
            print(f"Error while scraping description: {e}")



        try:
            # scraping key skills

            Key_skills = response.xpath("//*[@id='doverview']/div/div/div[2]/ul/li/text()").extract()
            Key_skills_string = ""
            for skill in Key_skills:
                Key_skills_string = Key_skills_string + skill + "|"
            Key_skills_string = Key_skills_string[:-1].strip().replace("  ", " ")
            print(Key_skills_string)

        except Exception as e:
            print(f"Error while scraping skills: {e}")



        try:
            # scraping Prerequitsites

            Prerequitsites = response.xpath("//*[@id='deligibility']/div/div/div/div/div[2]/div/div[1]/div/div/ul/li/text()").extract()
            Prerequitsites_text = ""
            for Prereq in Prerequitsites:
                Prereq = str(Prereq)
                Prereq = Prereq.strip()
                Prerequitsites_text = Prerequitsites_text + Prereq + " | "
            Prerequitsites_text = Prerequitsites_text[:-2].replace('  ', ' ')
            print(Prerequitsites_text)

            if Prerequitsites_text == "":
                Prerequitsites = response.xpath("//*[@id='deligibility']/div/div/div/div/div[2]/div/div[1]/div/div/p/text()").extract()
                Prerequitsites_text = ""
                for Prereq in Prerequitsites:
                    Prereq = str(Prereq).replace("\n", "").strip()
                    if Prereq != "." and Prereq != "" and Prereq != " ":
                        Prerequitsites_text = Prerequitsites_text + Prereq + ' | '
                Prerequitsites_text = Prerequitsites_text.replace('  ', ' ')
                Prerequitsites_text = Prerequitsites_text[:-2]
                print(Prerequitsites_text)

        except Exception as e:
            print(f"Error while scraping Prerequitsites: {e}")




        try:
            # scraping syllabus

            Syllabus = response.xpath("//*[@id='dsyllabus']/div/div/div/div/div[1]/div/ul/li/a/text()").extract()
            Final_syllabus_string = '<?xml version="1.0"?>\n<mainmodule>\n'
            for N, main_module in enumerate(Syllabus):
                N = N+1
                main_module = str(main_module).replace('\n','').strip()

                Sub_Syllabus_string = "  <subheading>\n"
                Sub_Syllabus = response.xpath(f"//*[@id='syl-tab{N}']/ul/li/text()").extract()
                if len(Sub_Syllabus) == 0:
                    Sub_Syllabus = response.xpath(f"//*[@id='syl-tab{N}']/p/text()").extract()
                    for n, sub_module in enumerate(Sub_Syllabus):
                        n = n+1
                        Sub_Syllabus_string = Sub_Syllabus_string + f"   <item{n}>{sub_module}</item{n}>\n"
                    Sub_Syllabus_string = Sub_Syllabus_string + "  </subheading>"
                    #print(Sub_Syllabus_string)

                    Final_syllabus_string = Final_syllabus_string+f" <module{N}>\n  <heading>{main_module}</heading>\n{Sub_Syllabus_string}\n </module{N}>\n"

                else:
                    for n, sub_module in enumerate(Sub_Syllabus):
                        n = n+1
                        Sub_Syllabus_string = Sub_Syllabus_string + f"   <item{n}>{sub_module}</item{n}>\n"
                    Sub_Syllabus_string = Sub_Syllabus_string + "  </subheading>"
                    #print(Sub_Syllabus_string)

                    Final_syllabus_string = Final_syllabus_string+f" <module{N}>\n  <heading>{main_module}</heading>\n{Sub_Syllabus_string}\n </module{N}>\n"


            Final_syllabus_string = Final_syllabus_string + "</mainmodule>"
            print(Final_syllabus_string)

        except Exception as e:
            print(f"Error while scraping syllabus: {e}")



        try:
            #scraping price

            Price = response.xpath("//*[@id='dfeestructure']/div/div/div[1]/div[3]/div[3]/div[1]/div[2]/text()").extract()
            Price = Price[0]
            Price = str(Price).replace("\n", "").strip().split()[1]
            Price = float(Price)
            Price = int(Price)
            print(Price)

        except:
            Price = response.xpath("//*[@id='dfeestructure']/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/text()").extract()
            Price = Price[0]
            Price = str(Price).replace("\n", "").strip().split()[1]
            Price = float(Price)
            Price = int(Price)
            print(Price)





        courses["Title"] = Full_Title_text
        courses["Short_Description"] = Full_Short_Description_string
        courses["Description"] = Description_para_string
        courses["Key_skills"] = Key_skills_string
        courses["Prerequitsites"] = Prerequitsites_text
        courses["syllabus"] = Final_syllabus_string
        courses["Price"] = Price

        yield courses





